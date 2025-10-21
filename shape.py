import pygame
import math

class Shape:
    def __init__(self, center, size=100):
        self.center = pygame.Vector2(center)
        self.width = size
        self.height = size
        self.anchor = pygame.Vector2(center)
        self.color = (200, 200, 200)
        self.rotation = 0  

    def draw(self, surface):
        points = self.get_corners_rotated()
        pygame.draw.polygon(surface, self.color, points, 2)

        for p in self.get_edge_midpoints(points):
            pygame.draw.circle(surface, (100, 200, 255), p, 5)

        for p in points:
            pygame.draw.circle(surface, (255, 255, 0), p, 6)

        pygame.draw.circle(surface, (255, 80, 80), self.anchor, 6)

    def get_corners_rotated(self):
        half_w = self.width / 2
        half_h = self.height / 2
        local_corners = [
            pygame.Vector2(-half_w, -half_h), 
            pygame.Vector2( half_w, -half_h),  
            pygame.Vector2( half_w,  half_h),  
            pygame.Vector2(-half_w,  half_h)   
        ]

        center_rotated = self.anchor + (self.center - self.anchor).rotate_rad(self.rotation)

        rotated = []
        for c in local_corners:
            rc = c.rotate_rad(self.rotation)
            rotated.append(rc + center_rotated)

        return rotated

    def get_edge_midpoints(self, corners):
        mids = []
        for i in range(4):
            a = corners[i]
            b = corners[(i + 1) % 4]
            mids.append(((a.x + b.x) / 2, (a.y + b.y) / 2))
        return mids

    def contains_point(self, point):
        visual_center = self.anchor + (self.center - self.anchor).rotate_rad(self.rotation)
        
        half_w = self.width / 2
        half_h = self.height / 2
        rect = pygame.Rect(
            visual_center.x - half_w, visual_center.y - half_h,
            self.width, self.height
        )
        return rect.collidepoint(point)

    def is_over_anchor(self, point):
        return (pygame.Vector2(point) - self.anchor).length() < 10

    def is_over_corner(self, point):
        for corner in self.get_corners_rotated():
            if (pygame.Vector2(point) - corner).length() < 10:
                return True
        return False

    def is_over_midpoint(self, point):
        corners = self.get_corners_rotated()
        midpoints = self.get_edge_midpoints(corners)
        for i, mid in enumerate(midpoints):
            if (pygame.Vector2(point) - pygame.Vector2(mid)).length() < 10:
                return i
        return None

    def move(self, delta):
        self.center += delta
        self.anchor += delta
    
    def set_anchor(self, new_anchor_pos):
        visual_center = self.anchor + (self.center - self.anchor).rotate_rad(self.rotation)
        self.anchor = new_anchor_pos
        self.center = self.anchor + (visual_center - self.anchor).rotate_rad(-self.rotation)
