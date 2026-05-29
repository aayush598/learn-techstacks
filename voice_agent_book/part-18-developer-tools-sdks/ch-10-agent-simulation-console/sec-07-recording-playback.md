# Section 07: Recording & Playback

## Overview

Recording and playback captures simulated conversations as audio recordings with synchronized transcripts. Playback controls include step-through debugging at the utterance level, timeline navigation, and configurable playback speed. Recordings are stored alongside simulation results for post-mortem analysis and compliance.

## Architecture

```
Recording & Playback System
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Simulation Engine] → [Recording Service] → [Storage]
       │                       │                 │
  Audio chunks +           Audio mixer         S3 bucket
  transcript segments      + metadata          + database
  with timestamps          + VAD markers
                            + speaker labels    DB: PostgreSQL
                                                  (metadata)

[Playback UI]
       │
  ┌────┴────┐
  │         │
  Player  Timeline
  ┌────┐   ┌────────────────────┐
  │ ▶  │   │Caller│  Agent │    │
  │ ⏸  │   │───  │  ──────│────│
  │ ⏹  │   │User  │  Resp  │   │
  │ ◀▶ │   │─────│──────│─────│
  │ ⏩ │   │Step 1│ Step 2│    │
  └────┘   └────────────────────┘

  Debug Panel (step-through):
  [STT] Input: "I want a refund"
  [NLU] Intent: refund_request (0.97)
  [Dialog] Action: request_order_details
  [TTS] Output: "I can help with that..."
```

## Design Decisions

- **Standalone Audio Files**: Each simulation produces a single merged audio file
- **Segment-Level Metadata**: Each utterance indexed with start/end timestamps
- **VAD-Based Segmentation**: Voice activity detection splits caller/agent segments
- **Cloud Storage**: Audio stored in S3 with signed URLs for playback

## Implementation Approach

```typescript
// Recording types
interface SimulationRecording {
  id: string;
  simulationId: string;
  scenarioName: string;
  audioUrl: string;         // Signed S3 URL
  durationSeconds: number;
  segments: AudioSegment[];
  transcript: TranscriptEntry[];
  metadata: {
    sampleRate: number;
    codec: string;
    channels: number;
    fileSize: number;
  };
  createdAt: Date;
}

interface AudioSegment {
  id: string;
  speaker: 'caller' | 'agent';
  startTime: number;        // Milliseconds from start
  endTime: number;
  text: string;
  confidence: number;       // ASR confidence
  wordTimings: WordTiming[];
}

interface TranscriptEntry {
  speaker: 'caller' | 'agent';
  text: string;
  timestamp: number;        // Milliseconds from start
  isVerificationStep: boolean;
  verificationResult?: 'passed' | 'failed';
}

// Recording service
class RecordingService {
  private audioMixer: AudioMixer;
  private s3: S3Client;

  async recordSimulation(
    simulationId: string,
    stepResults: StepResultData[],
  ): Promise<SimulationRecording> {
    // Collect audio chunks from each step
    const audioChunks: AudioChunk[] = [];
    const segments: AudioSegment[] = [];
    const transcript: TranscriptEntry[] = [];

    for (const step of stepResults) {
      if (step.callerInput) {
        // Generate synthetic audio for caller input
        const callerAudio = await this.synthesizeAudio(step.callerInput, 'caller');

        audioChunks.push({
          buffer: callerAudio,
          speaker: 'caller',
          text: step.callerInput,
          offset: this.getCurrentDuration(audioChunks),
        });

        segments.push({
          id: crypto.randomUUID(),
          speaker: 'caller',
          startTime: this.getCurrentDuration(audioChunks) - callerAudio.duration,
          endTime: this.getCurrentDuration(audioChunks),
          text: step.callerInput,
          confidence: 1.0,
          wordTimings: this.generateWordTimings(step.callerInput, callerAudio.duration),
        });

        transcript.push({
          speaker: 'caller',
          text: step.callerInput,
          timestamp: this.getCurrentDuration(audioChunks) - callerAudio.duration,
          isVerificationStep: false,
        });
      }

      if (step.agentResponse) {
        // Synthesize agent response audio
        const agentAudio = await this.synthesizeAudio(step.agentResponse, 'agent');

        audioChunks.push({
          buffer: agentAudio,
          speaker: 'agent',
          text: step.agentResponse,
          offset: this.getCurrentDuration(audioChunks),
        });

        segments.push({
          id: crypto.randomUUID(),
          speaker: 'agent',
          startTime: this.getCurrentDuration(audioChunks) - agentAudio.duration,
          endTime: this.getCurrentDuration(audioChunks),
          text: step.agentResponse,
          confidence: 1.0,
          wordTimings: this.generateWordTimings(step.agentResponse, agentAudio.duration),
        });

        transcript.push({
          speaker: 'agent',
          text: step.agentResponse,
          timestamp: this.getCurrentDuration(audioChunks) - agentAudio.duration,
          isVerificationStep: step.verificationResults.length > 0,
          verificationResult: step.status === 'passed' ? 'passed' : 'failed',
        });
      }
    }

    // Mix all audio chunks into single file
    const mixedAudio = await this.audioMixer.mix(audioChunks.map(c => c.buffer));

    // Upload to S3
    const audioUrl = await this.uploadAudio(simulationId, mixedAudio);

    return {
      id: crypto.randomUUID(),
      simulationId,
      scenarioName: stepResults[0]?.callerInput || 'Simulation',
      audioUrl,
      durationSeconds: mixedAudio.duration / 1000,
      segments,
      transcript,
      metadata: {
        sampleRate: 16000,
        codec: 'wav',
        channels: 1,
        fileSize: mixedAudio.byteLength,
      },
      createdAt: new Date(),
    };
  }

  private async synthesizeAudio(text: string, speaker: string): Promise<AudioBuffer> {
    const tts = new TtsEngine({ provider: 'simulation', voice: speaker === 'caller' ? 'default' : 'agent' });
    return tts.synthesize(text);
  }

  private async uploadAudio(simulationId: string, audio: AudioBuffer): Promise<string> {
    const key = `simulations/${simulationId}/recording.wav`;
    await this.s3.send(new PutObjectCommand({
      Bucket: process.env.SIMULATION_RECORDINGS_BUCKET,
      Key: key,
      Body: audio,
      ContentType: 'audio/wav',
    }));

    return this.s3.send(new GetObjectCommand({
      Bucket: process.env.SIMULATION_RECORDINGS_BUCKET,
      Key: key,
    })).$metadata.requestId;
  }
}

// Playback UI controller
function PlaybackController({ recording }: { recording: SimulationRecording }) {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [currentTime, setCurrentTime] = useState(0);
  const [activeSegment, setActiveSegment] = useState<string | null>(null);
  const [speed, setSpeed] = useState(1);
  const [isStepThrough, setIsStepThrough] = useState(false);
  const segmentsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const onTimeUpdate = () => {
      const time = audio.currentTime * 1000;
      setCurrentTime(time);

      // Highlight active segment
      const segment = recording.segments.find(
        s => time >= s.startTime && time <= s.endTime,
      );
      setActiveSegment(segment?.id || null);

      // Auto-scroll timeline
      if (segment && segmentsRef.current) {
        const el = segmentsRef.current.querySelector(`[data-segment-id="${segment.id}"]`);
        el?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    };

    audio.addEventListener('timeupdate', onTimeUpdate);
    return () => audio.removeEventListener('timeupdate', onTimeUpdate);
  }, [recording]);

  function stepForward() {
    const currentSegment = recording.segments.find(s =>
      currentTime >= s.startTime && currentTime <= s.endTime,
    );
    const currentIndex = currentSegment
      ? recording.segments.indexOf(currentSegment)
      : -1;
    const nextIndex = Math.min(currentIndex + 1, recording.segments.length - 1);
    const nextSegment = recording.segments[nextIndex];
    if (nextSegment && audioRef.current) {
      audioRef.current.currentTime = nextSegment.startTime / 1000;
      audioRef.current.play();
    }
  }

  function jumpToSegment(segment: AudioSegment) {
    if (audioRef.current) {
      audioRef.current.currentTime = segment.startTime / 1000;
    }
  }

  return (
    <div className="playback-container">
      <audio ref={audioRef} src={recording.audioUrl} />

      <div className="playback-controls">
        <button onClick={() => audioRef.current?.play()}>▶ Play</button>
        <button onClick={() => audioRef.current?.pause()}>⏸ Pause</button>
        <button onClick={() => { audioRef.current!.currentTime = 0; }}>⏹ Stop</button>

        <select value={speed} onChange={e => {
          setSpeed(Number(e.target.value));
          audioRef.current!.playbackRate = Number(e.target.value);
        }}>
          <option value={0.5}>0.5x</option>
          <option value={1}>1x</option>
          <option value={1.5}>1.5x</option>
          <option value={2}>2x</option>
        </select>

        <button onClick={() => setIsStepThrough(!isStepThrough)}>
          {isStepThrough ? '🚫 Step Mode' : '👣 Step Through'}
        </button>

        <button onClick={stepForward} disabled={!isStepThrough}>
          Step Forward
        </button>
      </div>

      <div className="playback-timeline">
        <input
          type="range"
          min={0}
          max={recording.durationSeconds * 1000}
          value={currentTime}
          onChange={e => {
            const time = Number(e.target.value);
            audioRef.current!.currentTime = time / 1000;
          }}
        />
      </div>

      <div className="transcript-timeline" ref={segmentsRef}>
        {recording.segments.map(segment => (
          <div
            key={segment.id}
            data-segment-id={segment.id}
            className={`transcript-segment ${segment.speaker} ${activeSegment === segment.id ? 'active' : ''}`}
            onClick={() => jumpToSegment(segment)}
          >
            <div className="segment-timestamp">
              {formatTime(segment.startTime)} - {formatTime(segment.endTime)}
            </div>
            <div className="segment-speaker">{segment.speaker === 'caller' ? '👤 Caller' : '🤖 Agent'}</div>
            <div className="segment-text">{segment.text}</div>
            <div className="segment-confidence">
              Confidence: {(segment.confidence * 100).toFixed(0)}%
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Integration Points

- **Simulation Results**: Recordings linked from simulation result detail pages
- **Debugging Workflow**: Step-through mode for detailed pipeline debugging
- **Compliance Storage**: Recordings retained for compliance auditing

## Production Considerations

- **Audio Storage Costs**: S3 lifecycle policies for automatic archival after 90 days
- **Signed URLs**: Pre-signed S3 URLs with 1-hour expiry for secure playback
- **Large File Handling**: Chunked loading for recordings longer than 30 minutes
- **Browser Compatibility**: Fallback to text-only view for browsers without audio support

## Open-Source Tools

- **WaveSurfer.js**: Audio waveform visualization
- **SoX (Sound eXchange)**: Audio processing and mixing
- **ffmpeg**: Audio codec conversion and processing
