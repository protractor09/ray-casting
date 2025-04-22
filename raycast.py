import pygame 
import math
import sys

FOV=math.pi/3
HALF_FOV=FOV/2
SCREEN_HEIGHT=480
SCREEN_WIDTH=960
TILE_SIZE=int((SCREEN_HEIGHT/2)/8)
M_T=8

CASTED_RAYS=160
DEPTH=int(M_T*TILE_SIZE)



p_x = (SCREEN_WIDTH / 2) / 2
p_y = (SCREEN_WIDTH / 2) / 2
p_a=math.pi


MAP=  ('########'
       '# #    #'    
       '# #  ###'    
       '#      #'   
       '##     #'   
       '#  ### #'   
       '#   #  #'  
       '########')


pygame.init()
window=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Ray-Caster")
clock=pygame.time.Clock()

def draw_map():
    light_grey = (191, 191, 191)
    dark_grey = (65, 65, 65)
    for i in range(M_T):
        for j in range(M_T):
            sq=i*M_T+j
            pygame.draw.rect(window,light_grey if MAP[sq]=='#' else dark_grey,(j*TILE_SIZE,i*TILE_SIZE,TILE_SIZE-1,TILE_SIZE-1))
    pygame.draw.circle(window,(0,0,0),(int(p_x),int(p_y)),7)


def raycast():
    start_angle=p_a-HALF_FOV
    for i in range(CASTED_RAYS):
        for j in range(DEPTH):
            t_x=p_x-math.sin(start_angle)*j #gives the target coords for x or where the ray should end
            t_y=p_y+math.cos(start_angle)*j #gives the target coords for y or where the ray should end
            
            col=int(t_x/TILE_SIZE) #convert to map coords
            row=int(t_y/TILE_SIZE)

            square=row*M_T + col #map sq indx
            if 0<=col<M_T and 0<=row<M_T:
                if MAP[square]=='#':
                    pygame.draw.line(window,'white',(p_x,p_y),(t_x,t_y))
                    break
        start_angle+=(FOV/CASTED_RAYS) # at what angle to make the next line




#movement direction
forward=True


while True:
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    draw_map()
    raycast()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        #working with radians, not degrees
        p_a -= 0.1
    elif keys[pygame.K_RIGHT]:
        p_a += 0.1
    elif keys[pygame.K_UP]:
        forward = True
        p_x += -1 * math.sin(p_a) * 5
        p_y += math.cos(p_a) * 5
    elif keys[pygame.K_DOWN]:
        forward = False
        p_x -= -1 * math.sin(p_a) * 5
        p_y -= math.cos(p_a) * 5
    pygame.display.flip()
    clock.tick(30)

