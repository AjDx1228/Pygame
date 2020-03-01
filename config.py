import pygame

screen_width = 200
screen_height = 600

background_image = 'images/background.jpg'

frame_rate = 60

lift_width = 80	
lift_height = 20	
lift_color = (0, 255, 0)	
lift_speed = 10	

player_width = 40	
player_height = 40	
player_color = (0, 255, 0)	
player_speed = 10	

box_width = 40	
box_height = 40	
box_color = (0, 123, 147)	
box_speed = 10

n_zones = int(screen_width / box_width)