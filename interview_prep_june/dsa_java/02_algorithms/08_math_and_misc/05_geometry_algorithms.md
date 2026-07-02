# Geometry Algorithms

## Point and Orientation

```java
class Point { int x, y; Point(int x, int y) { this.x = x; this.y = y; } }

// Cross product: returns +ve (CCW), -ve (CW), 0 (collinear)
int cross(Point a, Point b, Point c) {
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
}

// Check if point p lies on segment ab (assuming collinear)
boolean onSegment(Point a, Point b, Point p) {
    return p.x <= Math.max(a.x, b.x) && p.x >= Math.min(a.x, b.x)
        && p.y <= Math.max(a.y, b.y) && p.y >= Math.min(a.y, b.y);
}

// Check if segments a1-a2 and b1-b2 intersect
boolean intersect(Point a1, Point a2, Point b1, Point b2) {
    int o1 = cross(a1, a2, b1);
    int o2 = cross(a1, a2, b2);
    int o3 = cross(b1, b2, a1);
    int o4 = cross(b1, b2, a2);

    if (o1 != 0 || o2 != 0 || o3 != 0 || o4 != 0) {
        return (o1 > 0) != (o2 > 0) && (o3 > 0) != (o4 > 0);
    }
    // Collinear — check overlap
    return onSegment(a1, a2, b1) || onSegment(a1, a2, b2)
        || onSegment(b1, b2, a1) || onSegment(b1, b2, a2);
}
```

## Convex Hull (Monotone Chain)

```java
public List<Point> convexHull(Point[] points) {
    int n = points.length;
    if (n < 3) return Arrays.asList(points);

    Arrays.sort(points, (a, b) -> a.x != b.x ? a.x - b.x : a.y - b.y);

    List<Point> hull = new ArrayList<>();

    // Lower hull
    for (int i = 0; i < n; i++) {
        while (hull.size() >= 2
               && cross(hull.get(hull.size()-2), hull.get(hull.size()-1), points[i]) <= 0) {
            hull.remove(hull.size() - 1);
        }
        hull.add(points[i]);
    }

    // Upper hull
    int upperSize = hull.size();
    for (int i = n - 2; i >= 0; i--) {
        while (hull.size() > upperSize
               && cross(hull.get(hull.size()-2), hull.get(hull.size()-1), points[i]) <= 0) {
            hull.remove(hull.size() - 1);
        }
        hull.add(points[i]);
    }

    hull.remove(hull.size() - 1); // remove duplicate first point
    return hull;
}
```

## Area of Polygon (Shoelace Formula)

```java
public double polygonArea(List<Point> points) {
    int n = points.size();
    long area = 0;
    for (int i = 0; i < n; i++) {
        int j = (i + 1) % n;
        area += (long) points.get(i).x * points.get(j).y;
        area -= (long) points.get(j).x * points.get(i).y;
    }
    return Math.abs(area) / 2.0;
}
```
