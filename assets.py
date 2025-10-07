import pygame

def load_assets(WIDTH, HEIGHT):
    """
    Loads and transforms all game assets (images) using the screen dimensions.

    Args:
        WIDTH (int): The screen width.
        HEIGHT (int): The screen height.

    Returns:
        dict: A dictionary containing all the loaded and transformed assets.
    """
    assets = {}

    # --- Background and Ground ---
    background = pygame.image.load('assets/img/city_night_1.png').convert_alpha()
    # background = pygame.image.load('assets/img/weird_dungon.png').convert_alpha() # Alternative background
    assets['background_surf'] = pygame.transform.scale(background, (WIDTH, HEIGHT))
    assets['background_rect'] = assets['background_surf'].get_rect()

    ground = pygame.image.load('assets/img/ground-shane-1-wide.png')
    assets['ground_surf'] = pygame.transform.scale_by(ground, 4)
    # Positioning the ground to the bottom-center of the screen
    assets['ground_rect'] = assets['ground_surf'].get_rect(midbottom=(WIDTH // 2, HEIGHT))

    # --- Projectiles and Weapons ---
    assets['player_bullet_img'] = pygame.image.load('assets/img/bullet2.png').convert_alpha()
    assets['enemy_bullet_img'] = pygame.image.load('assets/img/enemy_bullet_circle1.png').convert_alpha()
    assets['shotgun_img'] = pygame.image.load('assets/img/shotgun_right.png').convert_alpha()
    assets['shotgun_img_yellow'] = pygame.image.load('assets/img/shotgun_yellow.png').convert_alpha()
    assets['shotgun_img_red'] = pygame.image.load('assets/img/shotgun_red.png').convert_alpha()
    assets['shotgun_img_purple'] = pygame.image.load('assets/img/shotgun_purple.png').convert_alpha()

    # --- Mob Enemies ---
    assets['mob_1_img'] = pygame.image.load('assets/img/drone_ball.png').convert_alpha()

    # Tank Guy Assets (scaled by 4)
    assets['tank_guy_img1'] = pygame.transform.scale_by(
        pygame.image.load('assets/img/tank_guy_red1.png').convert_alpha(), 4
    )
    assets['tank_guy_img2'] = pygame.transform.scale_by(
        pygame.image.load('assets/img/tank_guy_red2.png').convert_alpha(), 4
    )
    assets['tank_guy_img3'] = pygame.transform.scale_by(
        pygame.image.load('assets/img/tank_guy_red3.png').convert_alpha(), 4
    )
    assets['tank_guy_img4'] = pygame.transform.scale_by(
        pygame.image.load('assets/img/tank_guy_red4.png').convert_alpha(), 4
    )

    # Tank Guy Angled Assets (scaled by 4)
    assets['tank_guy_angle_img1'] = pygame.transform.scale_by(
        pygame.image.load('assets/img/tank_guy_angle1.png').convert_alpha(), 4
    )
    assets['tank_guy_angle_img2'] = pygame.transform.scale_by(
        pygame.image.load('assets/img/tank_guy_angle2.png').convert_alpha(), 4
    )
    assets['tank_guy_angle_img3'] = pygame.transform.scale_by(
        pygame.image.load('assets/img/tank_guy_angle3.png').convert_alpha(), 4
    )
    assets['tank_guy_angle_img4'] = pygame.transform.scale_by(
        pygame.image.load('assets/img/tank_guy_angle4.png').convert_alpha(), 4
    )

    # --- UI and Powerups ---
    assets['heart_red'] = pygame.image.load('assets/img/heart1.png').convert_alpha()
    assets['heart_red_empty'] = pygame.image.load('assets/img/heart1_fade.png').convert_alpha()

    # Rapid Fire Powerup (scaled by 2.5)
    rapid_img = pygame.image.load('assets/img/rapidfire_notext.png').convert_alpha()
    assets['rapid_powerup_img'] = pygame.transform.scale_by(rapid_img, 2.5)

    # Bounce Powerup (scaled by 2.5)
    bounce_img = pygame.image.load('assets/img/bounce_powerup_1.png').convert_alpha()
    assets['bounce_powerup_img'] = pygame.transform.scale_by(bounce_img, 2.5)

    return assets