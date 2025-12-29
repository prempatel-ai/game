in this i have provided diff design of main car 


1. Main first version of the car in this game:
    def draw_car(self):
        """Render the player's car with realistic details."""
        car_rect = self.get_car_rect()
        cx, cy = car_rect.x, car_rect.y
        
        # Shadow effect
        shadow = pygame.Surface((CAR_WIDTH + 4, CAR_HEIGHT + 4), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 60), (0, 0, CAR_WIDTH + 4, CAR_HEIGHT + 4), border_radius=8)
        self.screen.blit(shadow, (cx - 2, cy + 2))
        
        # Main car body with rounded corners
        pygame.draw.rect(self.screen, CAR_COLOR, car_rect, border_radius=6)
        
        # Car body highlights (3D effect)
        highlight_color = (255, 60, 90)
        pygame.draw.rect(self.screen, highlight_color, 
                        (cx + 2, cy + 2, CAR_WIDTH - 4, CAR_HEIGHT - 4), border_radius=5)
        
        # Car roof (darker shade)
        roof_color = (180, 15, 50)
        pygame.draw.rect(self.screen, roof_color, 
                        (cx + 8, cy + 20, CAR_WIDTH - 16, 30), border_radius=4)
        
        # Front windshield with gradient effect
        windshield_color = (100, 180, 255)
        windshield_dark = (60, 120, 200)
        
        # Front windshield
        pygame.draw.polygon(self.screen, windshield_dark, [
            (cx + 8, cy + 8),
            (cx + 32, cy + 8),
            (cx + 28, cy + 22),
            (cx + 12, cy + 22)
        ])
        pygame.draw.polygon(self.screen, windshield_color, [
            (cx + 10, cy + 10),
            (cx + 30, cy + 10),
            (cx + 27, cy + 21),
            (cx + 13, cy + 21)
        ])
        
        # Rear windshield
        pygame.draw.polygon(self.screen, windshield_dark, [
            (cx + 12, cy + 48),
            (cx + 28, cy + 48),
            (cx + 32, cy + 62),
            (cx + 8, cy + 62)
        ])
        pygame.draw.polygon(self.screen, windshield_color, [
            (cx + 13, cy + 49),
            (cx + 27, cy + 49),
            (cx + 30, cy + 61),
            (cx + 10, cy + 61)
        ])
        
        # Headlights
        pygame.draw.ellipse(self.screen, (255, 255, 200), (cx + 6, cy + 2, 8, 5))
        pygame.draw.ellipse(self.screen, (255, 255, 200), (cx + 26, cy + 2, 8, 5))
        
        # Taillights
        pygame.draw.ellipse(self.screen, (255, 0, 0), (cx + 6, cy + 63, 8, 5))
        pygame.draw.ellipse(self.screen, (255, 0, 0), (cx + 26, cy + 63, 8, 5))
        
        # Side mirrors
        pygame.draw.rect(self.screen, (150, 150, 150), (cx - 2, cy + 28, 3, 6))
        pygame.draw.rect(self.screen, (150, 150, 150), (cx + 39, cy + 28, 3, 6))
        
        # Door lines
        pygame.draw.line(self.screen, (150, 20, 40), (cx + 8, cy + 25), (cx + 8, cy + 55), 1)
        pygame.draw.line(self.screen, (150, 20, 40), (cx + 32, cy + 25), (cx + 32, cy + 55), 1)

2.  Bat man Vehicle here is design code:
    def draw_car(self):
        """Render the Hero Car as an armored Batmobile."""
        # Calculate coordinates based on lane position
        cx = int(ROAD_X + self.lane_index * LANE_WIDTH + (LANE_WIDTH - CAR_WIDTH) // 2 + self.car_x_offset)
        cy = int(self.car_y)
        w, h = CAR_WIDTH, CAR_HEIGHT
        screen = self.screen

        # Colors
        BLACK_ARMOR = (10, 10, 12)   # Near black with tiny blue tint
        DARK_GREY = (30, 30, 35)     # For armor plating definition
        TIRE_COLOR = (20, 20, 20)
        JET_ORANGE = (255, 140, 0)   # Exhaust glow
        JET_YELLOW = (255, 255, 150) # Exhaust center heat

        # --- 1. SHADOW (Grounding the heavy vehicle) ---
        shadow_surf = pygame.Surface((w + 20, h + 10), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 80), (0, 0, w + 20, h + 10))
        screen.blit(shadow_surf, (cx - 10, cy + 5))

        # --- 2. EXPOSED TIRES (Tumbler Style - draw first to be under body) ---
        # Front tires (narrower, tucked in)
        pygame.draw.rect(screen, TIRE_COLOR, (cx + 4, cy + 15, 8, 14), border_radius=3)
        pygame.draw.rect(screen, TIRE_COLOR, (cx + w - 12, cy + 15, 8, 14), border_radius=3)
        
        # Rear tires (MASSIVE, sticking out wider than the body base)
        rear_tire_y = cy + h - 25
        pygame.draw.rect(screen, TIRE_COLOR, (cx - 8, rear_tire_y, 12, 20), border_radius=4)
        pygame.draw.rect(screen, TIRE_COLOR, (cx + w - 4, rear_tire_y, 12, 20), border_radius=4)
        # Add tread detail lines
        pygame.draw.line(screen, (40,40,40), (cx - 8, rear_tire_y+5), (cx+4, rear_tire_y+5), 2)
        pygame.draw.line(screen, (40,40,40), (cx + w - 4, rear_tire_y+15), (cx+w+8, rear_tire_y+15), 2)

        # --- 3. MAIN ARMORED BODY ---
        # Aggressive, angular shape. Narrow nose, wide armored rear hips.
        body_pts = [
            (cx + w//2, cy),             # Nose tip point
            (cx + w, cy + 15),           # Front right flare
            (cx + w - 5, cy + 40),       # "Waist" tuck in
            (cx + w + 5, cy + h - 15),   # Rear right wide armor
            (cx + w//2, cy + h + 5),     # Tail point (jet housing)
            (cx - 5, cy + h - 15),       # Rear left wide armor
            (cx + 5, cy + 40),           # "Waist" tuck in
            (cx, cy + 15)                # Front left flare
        ]
        pygame.draw.polygon(screen, BLACK_ARMOR, body_pts)

        # --- 4. ARMOR PLATING DEFINITION (Highlights) ---
        # Subtle grey lines to show separate armor panels
        # Hood plating
        pygame.draw.line(screen, DARK_GREY, (cx + w//2, cy), (cx + 10, cy + 35), 1)
        pygame.draw.line(screen, DARK_GREY, (cx + w//2, cy), (cx + w - 10, cy + 35), 1)
        # Rear fender definition
        pygame.draw.line(screen, DARK_GREY, (cx - 5, cy + h - 15), (cx + 10, cy + 50), 1)
        pygame.draw.line(screen, DARK_GREY, (cx + w + 5, cy + h - 15), (cx + w - 10, cy + 50), 1)

        # --- 5. COCKPIT CANOPY ---
        # Small, armored, set far back.
        canopy_pts = [
            (cx + 12, cy + 35),
            (cx + w - 12, cy + 35),
            (cx + w - 15, cy + 55),
            (cx + 15, cy + 55)
        ]
        pygame.draw.polygon(screen, (5, 5, 10), canopy_pts) # Almost black glass
        # Slit windshield reflection
        pygame.draw.line(screen, (50, 50, 60), (cx + 18, cy + 40), (cx + w - 18, cy + 40), 2)

        # --- 6. REAR "BAT" FINS ---
        # Sharp angled fins on the rear fenders
        fin_color = (5, 5, 8)
        # Left fin
        pygame.draw.polygon(screen, fin_color, [(cx - 2, cy + h - 25), (cx - 8, cy + h), (cx + 5, cy + h - 10)])
        # Right fin
        pygame.draw.polygon(screen, fin_color, [(cx + w + 2, cy + h - 25), (cx + w + 8, cy + h), (cx + w - 5, cy + h - 10)])

        # --- 7. JET ENGINE EXHAUST ---
        # The massive central exhaust at the back
        jet_x, jet_y = cx + w//2, cy + h - 2
        # Outer metal ring
        pygame.draw.circle(screen, (40, 40, 40), (jet_x, jet_y), 9)
        # Inner orange glow
        pygame.draw.circle(screen, JET_ORANGE, (jet_x, jet_y), 6)
        # Center hot yellow core
        pygame.draw.circle(screen, JET_YELLOW, (jet_x, jet_y), 3)




3. Tesla Model s:
    def draw_car(self):
        """Render the Hero Car as a Tesla Model S Plaid."""
        # Calculate coordinates
        cx = int(ROAD_X + self.lane_index * LANE_WIDTH + (LANE_WIDTH - CAR_WIDTH) // 2 + self.car_x_offset)
        cy = int(self.car_y)
        w, h = CAR_WIDTH, CAR_HEIGHT
        screen = self.screen

        # --- FIX: Use Global CAR_COLOR instead of self.color ---
        BODY_COLOR = CAR_COLOR 
        GLASS_COLOR = (20, 20, 30) # Dark tinted glass
        TIRE_COLOR = (25, 25, 25)  # Dark Turbine wheels
        
        # --- 1. ELECTRIC UNDERGLOW ---
        # A clean "Electric Blue" halo
        glow_surf = pygame.Surface((w + 20, h + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (0, 100, 255, 40), (0, 0, w + 20, h + 20), border_radius=15)
        screen.blit(glow_surf, (cx - 10, cy - 10))

        # --- 2. TIRES (Turbine Wheels) ---
        # Tucked inside the body for aero
        wheel_positions = [
            (cx + 2, cy + 12),      # Front Left
            (cx + w - 8, cy + 12),  # Front Right
            (cx + 2, cy + h - 20),  # Rear Left
            (cx + w - 8, cy + h - 20) # Rear Right
        ]
        for wx, wy in wheel_positions:
            pygame.draw.rect(screen, TIRE_COLOR, (wx, wy, 6, 14), border_radius=2)

        # --- 3. MAIN BODY (Smooth Aero Shape) ---
        # We use a rounded rect for that smooth EV look, no sharp polygons
        # Main fuselage
        pygame.draw.rect(screen, BODY_COLOR, (cx, cy, w, h), border_radius=12)
        
        # Slight widening at rear wheel arches ("Hips")
        # We draw small arcs or rects on the side to simulate width without making it blocky
        pygame.draw.rect(screen, BODY_COLOR, (cx - 1, cy + h - 25, 3, 15), border_top_left_radius=2, border_bottom_left_radius=2)
        pygame.draw.rect(screen, BODY_COLOR, (cx + w - 2, cy + h - 25, 3, 15), border_top_right_radius=2, border_bottom_right_radius=2)

        # --- 4. PANORAMIC GLASS ROOF ---
        # The Model S has a huge glass top.
        # It narrows slightly towards the back.
        roof_pts = [
            (cx + 6, cy + 18),      # Front Left
            (cx + w - 6, cy + 18),  # Front Right
            (cx + w - 8, cy + h - 12), # Rear Right
            (cx + 8, cy + h - 12)   # Rear Left
        ]
        pygame.draw.polygon(screen, GLASS_COLOR, roof_pts)
        
        # Reflection line on the glass
        pygame.draw.line(screen, (50, 60, 80), (cx + 10, cy + 25), (cx + 14, cy + 35), 2)

        # --- 5. FRUNK (Front Trunk) ---
        # Subtle lines to define the hood
        pygame.draw.line(screen, (0, 0, 0), (cx + 10, cy + 18), (cx + w - 10, cy + 18), 1) # Base of windshield
        # The curved nose line
        pygame.draw.arc(screen, (0, 0, 0), (cx + 8, cy + 5, w - 16, 10), 0, 3.14, 1)

        # --- 6. LIGHTS ---
        # Headlights: Sleek, modern LED strips
        pygame.draw.line(screen, (220, 240, 255), (cx + 4, cy + 8), (cx + 12, cy + 5), 2)
        pygame.draw.line(screen, (220, 240, 255), (cx + w - 4, cy + 8), (cx + w - 12, cy + 5), 2)

        # Taillights: The signature bar + side wrap
        # Dark red for the off-state/housing
        pygame.draw.rect(screen, (100, 0, 0), (cx + 4, cy + h - 4, w - 8, 3), border_radius=1)
        # Bright red active light
        pygame.draw.line(screen, (255, 0, 0), (cx + 4, cy + h - 3), (cx + w - 4, cy + h - 3), 1)

        # --- 7. DETAILS ---
        # Side Mirrors (Body Colored, folded slightly for aero)
        pygame.draw.rect(screen, BODY_COLOR, (cx - 2, cy + 22, 3, 5), border_radius=1)
        pygame.draw.rect(screen, BODY_COLOR, (cx + w - 1, cy + 22, 3, 5), border_radius=1)
        
        # Tesla Logo (Abstract Silver Dot on nose)
        pygame.draw.circle(screen, (192, 192, 192), (cx + w//2, cy + 4), 2)


4. waymo car design :
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



for traffic defualt i have designed was :
     def draw(self, screen):
        """Render the traffic car with realistic appearance."""
        cx, cy = int(self.x), int(self.y)
        
        # Shadow
        shadow = pygame.Surface((self.width + 3, self.height + 3), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 50), (0, 0, self.width + 3, self.height + 3), border_radius=6)
        screen.blit(shadow, (cx - 1, cy + 2))
        
        # Main body with rounded corners
        pygame.draw.rect(screen, self.color, (cx, cy, self.width, self.height), border_radius=5)
        
        # Body highlight
        highlight = (60, 170, 255)
        pygame.draw.rect(screen, highlight, (cx + 2, cy + 2, self.width - 4, self.height - 4), border_radius=4)
        
        # Roof
        roof_color = (20, 100, 180)
        pygame.draw.rect(screen, roof_color, (cx + 8, cy + 20, self.width - 16, 30), border_radius=3)
        
        # Front windshield (angled)
        windshield = (150, 220, 255)
        pygame.draw.polygon(screen, (100, 150, 200), [
            (cx + 8, cy + 8), (cx + 32, cy + 8), (cx + 28, cy + 22), (cx + 12, cy + 22)
        ])
        pygame.draw.polygon(screen, windshield, [
            (cx + 10, cy + 10), (cx + 30, cy + 10), (cx + 27, cy + 21), (cx + 13, cy + 21)
        ])
        
        # Rear windshield
        pygame.draw.polygon(screen, (100, 150, 200), [
            (cx + 12, cy + 48), (cx + 28, cy + 48), (cx + 32, cy + 62), (cx + 8, cy + 62)
        ])
        pygame.draw.polygon(screen, windshield, [
            (cx + 13, cy + 49), (cx + 27, cy + 49), (cx + 30, cy + 61), (cx + 10, cy + 61)
        ])
        
        # Headlights
        pygame.draw.ellipse(screen, (255, 255, 150), (cx + 6, cy + 2, 8, 5))
        pygame.draw.ellipse(screen, (255, 255, 150), (cx + 26, cy + 2, 8, 5))
        
        # Taillights
        pygame.draw.ellipse(screen, (200, 0, 0), (cx + 6, cy + 63, 8, 5))
        pygame.draw.ellipse(screen, (200, 0, 0), (cx + 26, cy + 63, 8, 5))
        
        # Side mirrors
        pygame.draw.rect(screen, (120, 120, 120), (cx - 2, cy + 28, 3, 6))
        pygame.draw.rect(screen, (120, 120, 120), (cx + 39, cy + 28, 3, 6))




2. and Arcade Sports Car :
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