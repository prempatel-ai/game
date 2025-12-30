"""
2D Highway Driving Game - Overtaking Style
A realistic highway driving game where you overtake slower traffic

Controls:
- Arrow Keys OR WASD: Control car
  * UP/W: Speed up
  * DOWN/S: Slow down
  * LEFT/A: Change lane left
  * RIGHT/D: Change lane right
- ESC: Quit game

By Prem Patel  
"""

import sys
import random
import pygame
import tensorflow as tf

pygame.init()

# ============================================================
#                   Global Configuration
# ============================================================

# Screen & Roadfi
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
ROAD_WIDTH = 500
ROAD_X = (SCREEN_WIDTH - ROAD_WIDTH) // 2

LANE_COUNT = 3
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT

# Car dimensions
CAR_WIDTH, CAR_HEIGHT = 40, 70

# Colors
BG_COLOR = (34, 139, 34)        # Grass green
ROAD_COLOR = (60, 60, 60)       # Dark gray road
LINE_COLOR = (255, 255, 100)    # Yellow lines
CAR_COLOR = (220, 20, 60)       # Crimson red player car
OBSTACLE_COLOR = (30, 144, 255) # Dodger blue traffic
TEXT_COLOR = (255, 255, 255)    # White

# Game settings
PLAYER_BASE_SPEED = 0           # Player's forward speed
MIN_PLAYER_SPEED = 0
MAX_PLAYER_SPEED = 20
TRAFFIC_MIN_SPEED = 5          # Slower traffic to overtake
TRAFFIC_MAX_SPEED = 9
SPAWN_INTERVAL = 1000           # milliseconds between spawns

# ============================================================
#                    Planing for implementation of agent
# ============================================================

# reset
# reward
# we need to change play(action) so that -> agent can change lanes
# game_iteration
# and last to check is if it is collision  function

# ============================================================
#                    Traffic Car Class
# ============================================================

class TrafficCar:
    """Represents slower traffic cars to overtake."""
    
    def __init__(self, lane):
        self.width = 40
        self.height = 70
        self.speed = random.uniform(TRAFFIC_MIN_SPEED, TRAFFIC_MAX_SPEED)
        self.color = OBSTACLE_COLOR
        self.lane = lane
        
        # Position in the specified lane
        self.x = ROAD_X + lane * LANE_WIDTH + (LANE_WIDTH - self.width) // 2
        # Spawn ahead of player (at top of screen)
        self.y = -self.height
    
    def update(self, player_speed):
        """
        Update position relative to player's speed.
        Traffic moves slower, so player appears to overtake them.
        """
        # Relative speed = player speed - traffic speed
        # This makes traffic appear to move backward relative to player
        self.y += player_speed - self.speed
    
    def check_collision_with_traffic(self, other_cars):
        """
        Check if this car is colliding with other traffic cars.
        Adjust speed to maintain safe distance (realistic physics).
        """
        my_rect = self.get_rect()
        
        for other in other_cars:
            if other is self:  # Don't check collision with self
                continue
            
            # Only check cars in the same lane
            if other.lane == self.lane:
                other_rect = other.get_rect()
                
                # Check if cars are too close (within collision range)
                # We need to check vertical distance
                vertical_distance = abs(self.y - other.y)
                
                # If too close and this car is behind the other
                if vertical_distance < self.height + 10 and self.y > other.y:
                    # Match speed with car ahead to maintain safe distance
                    self.speed = min(self.speed, other.speed)
                    # Maintain minimum gap
                    if vertical_distance < self.height + 5:
                        self.y = other.y + other.height + 5
    
    def draw(self, screen):
        """Render traffic as a realistic Retro-Arcade Sports Car."""
        cx, cy = int(self.x), int(self.y)
        w, h = self.width, self.height
        
        # --- COLORS ---
        # We derive shades from the car's base color for a 3D effect
        base = self.color
        # Darker shade for sides/outline
        dark = (max(0, base[0]-60), max(0, base[1]-60), max(0, base[2]-60))
        # Lighter shade for hood highlights
        light = (min(255, base[0]+40), min(255, base[1]+40), min(255, base[2]+40))
        
        BLACK = (15, 15, 15)
        GLASS = (20, 25, 30)       # Dark tinted glass
        HEADLIGHT_GREY = (200, 200, 200) # Pop-up lights

        # --- 1. SHADOW ---
        shadow_surf = pygame.Surface((w + 4, h + 4), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (0, 0, 0, 60), (0, 0, w + 4, h + 4), border_radius=4)
        screen.blit(shadow_surf, (cx - 2, cy + 4))

        # --- 2. TIRES (Pixel Style) ---
        # Just small dark nubs sticking out slightly
        tire_positions = [cy + 12, cy + h - 18]
        for ty in tire_positions:
            pygame.draw.rect(screen, (25, 25, 25), (cx - 2, ty, 4, 10)) # Left
            pygame.draw.rect(screen, (25, 25, 25), (cx + w - 2, ty, 4, 10)) # Right

        # --- 3. CHASSIS BODY ---
        # Draw the darker base first (acts as the side skirts/outline)
        pygame.draw.rect(screen, dark, (cx, cy, w, h), border_radius=5)
        # Draw the main top surface (slightly inset to reveal dark sides)
        pygame.draw.rect(screen, base, (cx + 3, cy, w - 6, h - 2), border_radius=3)

        # --- 4. HOOD DETAILS (The "V" Shape) ---
        # Draw a lighter defined hood area
        hood_poly = [
            (cx + 6, cy + 25),          # Bottom Left of hood
            (cx + w - 6, cy + 25),      # Bottom Right of hood
            (cx + w - 8, cy + 4),       # Top Right
            (cx + 8, cy + 4)            # Top Left
        ]
        pygame.draw.polygon(screen, light, hood_poly)
        
        # Center Hood Vent (Dark line down the middle)
        pygame.draw.rect(screen, dark, (cx + w//2 - 1, cy + 6, 2, 15))

        # --- 5. POP-UP HEADLIGHTS ---
        # The signature square lights at the front
        pygame.draw.rect(screen, HEADLIGHT_GREY, (cx + 4, cy + 2, 7, 7), border_radius=1)
        pygame.draw.rect(screen, HEADLIGHT_GREY, (cx + w - 11, cy + 2, 7, 7), border_radius=1)
        
        # Grid pattern inside lights
        pygame.draw.line(screen, (150, 150, 150), (cx + 4, cy + 5), (cx + 11, cy + 5), 1)
        pygame.draw.line(screen, (150, 150, 150), (cx + w - 11, cy + 5), (cx + w - 4, cy + 5), 1)

        # --- 6. CABIN (Glass) ---
        # Front Windshield (Dark trapezoid)
        glass_points = [
            (cx + 5, cy + 26),        # Front Left
            (cx + w - 5, cy + 26),    # Front Right
            (cx + w - 7, cy + 42),    # Back Right
            (cx + 7, cy + 42)         # Back Left
        ]
        pygame.draw.polygon(screen, GLASS, glass_points)
        
        # Windshield Glare (The white streak)
        pygame.draw.line(screen, (200, 220, 230), (cx + 8, cy + 28), (cx + 12, cy + 38), 2)

        # Roof (Body colored block)
        pygame.draw.rect(screen, base, (cx + 6, cy + 42, w - 12, 14))
        
        # Rear Window (Smaller dark rectangle)
        pygame.draw.rect(screen, GLASS, (cx + 7, cy + 56, w - 14, 6))

        # --- 7. REAR SPOILER ---
        # The black wing at the back (iconic to your image)
        spoiler_y = cy + h - 9
        # Wing supports
        pygame.draw.rect(screen, dark, (cx + 6, spoiler_y - 2, 3, 3))
        pygame.draw.rect(screen, dark, (cx + w - 9, spoiler_y - 2, 3, 3))
        # The Main Wing
        pygame.draw.rect(screen, BLACK, (cx + 2, spoiler_y, w - 4, 6), border_radius=2)

        # --- 8. TAILLIGHTS & EXHAUST ---
        # Red strip under the spoiler
        pygame.draw.rect(screen, (220, 0, 0), (cx + 5, cy + h - 3, w - 10, 2))
        
        # Exhaust pipe (Tiny grey dot at bottom center)
        pygame.draw.circle(screen, (80, 80, 80), (cx + w//2 - 2, cy + h + 1), 2)
        pygame.draw.circle(screen, (80, 80, 80), (cx + w//2 + 2, cy + h + 1), 2)
    
    def get_rect(self):
        """Return collision rectangle."""
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
    
    def is_off_screen(self):
        """Check if car has moved past the bottom of screen."""
        return self.y > SCREEN_HEIGHT
    
    def is_near_top(self, threshold=200):
        """Check if car is still near the top of screen."""
        return self.y < threshold


# ============================================================
#                   Highway Game Class
# ============================================================

class HighwayGame:
    """Main game class handling overtaking gameplay."""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2d-Self-driving car's simulater")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Setup traffic spawn timer
        self.SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_EVENT, SPAWN_INTERVAL)
        
        self.reset()
    
    def reset(self):
        """Reset game state."""
        self.lane_index = 1  # Start in middle lane
        self.target_lane = 1  # Lane we're moving towards
        self.car_x_offset = 0  # Smooth position offset for lane transitions
        self.car_y = SCREEN_HEIGHT - 150  # Player position
        self.speed = PLAYER_BASE_SPEED
        self.road_offset = 0
        self.traffic = []
        self.score = 0
        self.overtakes = 0  # Count successful overtakes
        self.game_over = False
        self.is_changing_lane = False
    
    def handle_input(self):
        """Process keyboard input for speed control."""
        keys = pygame.key.get_pressed()
        
        # Speed control - Arrow keys OR WASD
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.speed = min(self.speed + 0.15, MAX_PLAYER_SPEED)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed = max(self.speed - 0.15, MIN_PLAYER_SPEED)
    
    def handle_lane_change(self, event):
        """Handle lane change input with key press events - Arrow keys OR WASD."""
        if event.type == pygame.KEYDOWN and not self.is_changing_lane:
            # Left lane change: LEFT arrow OR A key
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.target_lane > 0:
                self.target_lane -= 1
                self.is_changing_lane = True
            # Right lane change: RIGHT arrow OR D key
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.target_lane < LANE_COUNT - 1:
                self.target_lane += 1
                self.is_changing_lane = True
    
    def update(self):
        """Update game state."""
        if self.game_over:
            return
        
        # Smooth lane transition ( Need to work on this transition to add an smooth tilt on side which side car in which side it want to go )
        if self.is_changing_lane:
            target_x = ROAD_X + self.target_lane * LANE_WIDTH + (LANE_WIDTH - CAR_WIDTH) // 2
            current_x = ROAD_X + self.lane_index * LANE_WIDTH + (LANE_WIDTH - CAR_WIDTH) // 2 + self.car_x_offset
            
            transition_speed = 8
            
            if abs(target_x - current_x) < transition_speed:
                self.lane_index = self.target_lane
                self.car_x_offset = 0
                self.is_changing_lane = False
            else:
                if target_x > current_x:
                    self.car_x_offset += transition_speed
                else:
                    self.car_x_offset -= transition_speed
        
        # Update traffic cars
        player_rect = self.get_car_rect()
        
        # First pass: Check traffic-to-traffic collisions (realistic physics)
        for car in self.traffic:
            car.check_collision_with_traffic(self.traffic)
        
        # Second pass: Update positions
        for car in self.traffic[:]:
            old_y = car.y
            car.update(self.speed)
            
            # Check if we successfully overtook this car
            if old_y < self.car_y and car.y >= self.car_y and not car.is_off_screen():
                self.overtakes += 1
                self.score += 15  # Bonus for overtaking
            
            # Remove cars that went off screen
            """ personally  i really want to keep car that we overken and disappered from screen but there is problem like it will apper from behind and can crash to car player's  car.
             if i keep that it will looks more realistic i need more time to think on this 
             i have idea like implement that  other traffic car detect player car and keep distance between them  but need time to work on this  """ 
            if car.is_off_screen():
                self.traffic.remove(car)
                self.score += 5  # Small score for distance
        
        # Check collisions
        for car in self.traffic:
            if player_rect.colliderect(car.get_rect()):
                self.game_over = True
                break
        
        # Update road animation - moves backward since we're moving forward
        self.road_offset = (self.road_offset + self.speed) % 50
    
    def get_car_rect(self):
        """Get player car's collision rectangle with smooth lane transitions."""
        x = ROAD_X + self.lane_index * LANE_WIDTH + (LANE_WIDTH - CAR_WIDTH) // 2 + self.car_x_offset
        return pygame.Rect(int(x), self.car_y, CAR_WIDTH, CAR_HEIGHT)
    
    def draw_road(self):
        """Render the road and lane markings."""
        # Grass background
        self.screen.fill(BG_COLOR)
        
        # Road surface
        pygame.draw.rect(self.screen, ROAD_COLOR, (ROAD_X, 0, ROAD_WIDTH, SCREEN_HEIGHT))
        
        # Road borders
        pygame.draw.line(self.screen, LINE_COLOR, (ROAD_X, 0), (ROAD_X, SCREEN_HEIGHT), 4)
        pygame.draw.line(self.screen, LINE_COLOR, 
                         (ROAD_X + ROAD_WIDTH, 0), (ROAD_X + ROAD_WIDTH, SCREEN_HEIGHT), 4)
        
        # Lane markings (animated dashed lines moving backward)
        dash_height = 30
        gap = 20
        
        for lane in range(1, LANE_COUNT):
            x = ROAD_X + lane * LANE_WIDTH
            for y in range(-dash_height, SCREEN_HEIGHT, dash_height + gap):
                pygame.draw.line(
                    self.screen, LINE_COLOR,
                    (x, y + self.road_offset),
                    (x, y + dash_height + self.road_offset), 3
                )
    
    def draw_car(self):
        """Render the Hero Car as a Waymo (Jaguar I-PACE style) with LiDAR."""
        # Calculate coordinates
        cx = int(ROAD_X + self.lane_index * LANE_WIDTH + (LANE_WIDTH - CAR_WIDTH) // 2 + self.car_x_offset)
        cy = int(self.car_y)
        w, h = CAR_WIDTH, CAR_HEIGHT
        screen = self.screen

        # Colors
        WAYMO_WHITE = (245, 245, 245) # Classic Waymo White
        SENSOR_BLACK = (10, 10, 10)
        GLASS_COLOR = (20, 25, 30)
        LIDAR_GLOW = (0, 255, 100) # Tech Green/Cyan scanning color

        # --- 1. SHADOW ---
        shadow_surf = pygame.Surface((w + 10, h + 10), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 60), (0, 0, w + 10, h + 10))
        screen.blit(shadow_surf, (cx - 5, cy + 2))

        # --- 2. TIRES ---
        wheel_positions = [
            (cx, cy + 10),           # Front Left
            (cx + w - 6, cy + 10),   # Front Right
            (cx, cy + h - 18),       # Rear Left
            (cx + w - 6, cy + h - 18)# Rear Right
        ]
        for wx, wy in wheel_positions:
            pygame.draw.rect(screen, (30, 30, 30), (wx, wy, 6, 12), border_radius=2)

        # --- 3. MAIN BODY (SUV Shape) ---
        # Slightly boxier/wider at the back for the I-PACE look
        pygame.draw.rect(screen, WAYMO_WHITE, (cx, cy, w, h), border_radius=10)
        
        # --- 4. CORNER SENSORS (The "Waymo" Signature) ---
        # Little black pods on the 4 corners
        sensor_size = 4
        # Front Left
        pygame.draw.rect(screen, SENSOR_BLACK, (cx - 2, cy + 8, sensor_size, sensor_size + 4), border_radius=1)
        # Front Right
        pygame.draw.rect(screen, SENSOR_BLACK, (cx + w - 2, cy + 8, sensor_size, sensor_size + 4), border_radius=1)
        # Rear Left
        pygame.draw.rect(screen, SENSOR_BLACK, (cx - 2, cy + h - 15, sensor_size, sensor_size + 4), border_radius=1)
        # Rear Right
        pygame.draw.rect(screen, SENSOR_BLACK, (cx + w - 2, cy + h - 15, sensor_size, sensor_size + 4), border_radius=1)

        # --- 5. GLASS ROOF & WINDSHIELD ---
        # Large panoramic glass
        glass_pts = [
            (cx + 6, cy + 15),     # Front Left
            (cx + w - 6, cy + 15), # Front Right
            (cx + w - 8, cy + h - 10), # Rear Right
            (cx + 8, cy + h - 10)  # Rear Left
        ]
        pygame.draw.polygon(screen, GLASS_COLOR, glass_pts)

        # --- 6. LIDAR DOME (The Roof Scanner) ---
        # The main cylinder on top
        lidar_x, lidar_y = cx + w//2, cy + h//2 - 5
        
        # Base of LiDAR
        pygame.draw.circle(screen, (50, 50, 50), (lidar_x, lidar_y), 7)
        # Top of LiDAR (Black)
        pygame.draw.circle(screen, (0, 0, 0), (lidar_x, lidar_y), 5)
        
        # "Scanning" Effect - A rotating line or pulse
        # We use current time to animate the angle
        import math
        time_now = pygame.time.get_ticks()
        angle = (time_now % 1000) / 1000.0 * 6.28 # Full rotation every 1 second
        
        scan_x = lidar_x + math.cos(angle) * 5
        scan_y = lidar_y + math.sin(angle) * 5
        pygame.draw.line(screen, LIDAR_GLOW, (lidar_x, lidar_y), (scan_x, scan_y), 2)

        # --- 7. WAYMO / JAGUAR LOGO DETAILS ---
        # Jaguar "Grille" emblem
        pygame.draw.rect(screen, (20, 20, 20), (cx + 12, cy + 2, w - 24, 4), border_radius=2)
        # Red Growler logo dot
        pygame.draw.circle(screen, (200, 0, 0), (cx + w//2, cy + 4), 2)

        # Rear Taillights (Sleek horizontal lines)
        pygame.draw.rect(screen, (200, 0, 0), (cx + 4, cy + h - 4, 10, 3))
        pygame.draw.rect(screen, (200, 0, 0), (cx + w - 14, cy + h - 4, 10, 3))

    def draw_ui(self):
        """Render score and game information."""
        # Score and overtakes
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (20, 20))
        
        overtake_text = self.small_font.render(f"Overtakes: {self.overtakes}", True, TEXT_COLOR)
        self.screen.blit(overtake_text, (20, 60))
        
        # Speed indicator
        speed_text = self.small_font.render(f"Speed: {int(self.speed)}", True, TEXT_COLOR)
        self.screen.blit(speed_text, (20, 90))
        
        # Game over screen
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("CRASH!", True, (255, 50, 50))
            final_score_text = self.font.render(f"Final Score: {self.score}", True, TEXT_COLOR)
            overtakes_text = self.small_font.render(f"Total Overtakes: {self.overtakes}", True, TEXT_COLOR)
            restart_text = self.small_font.render("Press R to Restart or ESC to Quit", True, TEXT_COLOR)
            
            self.screen.blit(game_over_text, 
                           (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 180))
            self.screen.blit(final_score_text, 
                           (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, 240))
            self.screen.blit(overtakes_text, 
                           (SCREEN_WIDTH // 2 - overtakes_text.get_width() // 2, 280))
            self.screen.blit(restart_text, 
                           (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 340))
    
    def render(self):
        """Main rendering function."""
        self.draw_road()
        
        # Draw all traffic cars
        for car in self.traffic:
            car.draw(self.screen)
        
        self.draw_car()
        self.draw_ui()
        
        pygame.display.flip()
        self.clock.tick(60)  # 60 FPS
    
    def get_safe_spawn_lane(self):
        """
        Find a safe lane to spawn traffic that won't block all paths.
        Uses stricter checking to ensure player always has escape route.
        """
        # Check a larger danger zone at the top of screen
        DANGER_ZONE = 200  # Increased from 150
        
        # Get lanes that have traffic in the danger zone
        blocked_lanes = set()
        for car in self.traffic:
            if car.y < DANGER_ZONE:  # Car is in danger zone
                blocked_lanes.add(car.lane)
        
        # Get available safe lanes
        available_lanes = [i for i in range(LANE_COUNT) if i not in blocked_lanes]
        
        # If less than 2 lanes available, don't spawn (keep it safe)
        if len(available_lanes) < 2:
            return None  # Signal to skip spawning this time
        
        # Randomly choose from available safe lanes
        return random.choice(available_lanes)
    
    def should_spawn_traffic(self):
        """
        Additional check to prevent spawning when screen is too crowded.
        Returns True if it's safe to spawn new traffic.
        """
        # Count cars in upper half of screen
        cars_in_upper_half = sum(1 for car in self.traffic if car.y < SCREEN_HEIGHT // 2)
        
        # Don't spawn if too many cars already in upper area
        MAX_CARS_UPPER = 8
        return cars_in_upper_half < MAX_CARS_UPPER


# ============================================================
#                         Main Game Loop
# ============================================================

def main():
    """Main game loop."""
    game = HighwayGame()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Spawn traffic at regular intervals with safety checks
            if event.type == game.SPAWN_EVENT and not game.game_over:
                # Only spawn if it's safe to do so
                if game.should_spawn_traffic():
                    lane = game.get_safe_spawn_lane()
                    # Only spawn if we found a safe lane (not None)
                    if lane is not None:
                        game.traffic.append(TrafficCar(lane))
            
            # Keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                # Restart game
                if event.key == pygame.K_r and game.game_over:
                    game.reset()
                
                # Handle lane changes
                if not game.game_over:
                    game.handle_lane_change(event)
        
        # Game logic
        if not game.game_over:
            game.handle_input()
        game.update()
        game.render()
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()