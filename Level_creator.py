import json
import pygame
from Super_Classes.Screen import create_screen
from Super_Classes.Interface import Level as lv
from Basic_elements.Stars import Star
    
def follow_mous(st):
    m_pos = pygame.mouse.get_pos()
    st.pos = m_pos

def lock_star(st):
    st.text = st.create_text(st.text.content)
    star_list.append(st)

def save_to_json(name, id):
    path = lv.get_file_path(lv, str(name)+'.json')
    dictionary = {
        "constellation": [
        {
            "constellation_name": f"{name}",
            "constellation_id": id
        }
        ]
    }
    for indx, element in enumerate(star_list):
        new_star = {
            f"Star_{indx+1}": [
            {
                "pos":  element.pos,
                "radius": element.radius,
                "brightness": element.bright,
                "active": 1
            }
            ]
        }
        dictionary.update(new_star)
    ins = {"Instructions": [
        {
            "Connections": [[1,0]]
        }
    ]}
    dictionary.update(ins)
    e_text = {"Explanation_text": [
        {
            "Wo/Wann?: ": "a b",
            "Nachbarsternbilder: ": "a b",
            "Lateinischer Name: ": "a b",
            "Mythologie: ": "a b"
        }
    ]}
    dictionary.update(e_text)
    with open(path, "w") as outfile:
        json.dump(dictionary, outfile)
        

if(__name__ == "__main__"):
    create_screen()
    name = "Wasserschlange"
    id = 11
    image = pygame.image.load(lv.get_file_path(lv,str(name)+'.png'))
    star = Star((500,500),20,0.5,True,1,"1","")
    screen = pygame.display.get_surface()
    star_list = []
    count_stars = 1
    Running = True
    freeze = False
    
    while Running: 
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    star = Star((500,500),20,0.5,True, count_stars,f"{count_stars}","")
                    star.draw()    

                if event.key == pygame.K_KP_PLUS:
                    star.radius += 1
                
                if event.key == pygame.K_KP_MINUS:
                    star.radius -= 1
                
                if event.key == pygame.K_UP:
                    if star.bright - 0.05 < 0:
                        pass
                    else:
                        bright = star.bright - 0.05
                        star.bright = bright
                        star.color = (255-(bright*255),255-(bright*255),255-(bright*255))
                    
                
                if event.key == pygame.K_DOWN:
                    if star.bright + 0.05 > 1:
                        pass
                    else:
                        bright = star.bright + 0.05
                        star.bright = bright
                        star.color = (255-(bright*255),255-(bright*255),255-(bright*255))
                
                if event.key == pygame.K_DELETE:
                    count_stars -=1
                    if count_stars < 0:
                        count_stars = 0
                    star = Star((500,500),20, 0.5, True, count_stars, f"{count_stars}", "")
                    star_list = star_list[:-1]
                
                if event.key == pygame.K_RETURN:
                    save_to_json(name, id)
                    

            if pygame.mouse.get_pressed()[0]:
                    lock_star(star)
                    count_stars +=1
                    star = Star((500,500),20, 0.5, True, count_stars, f"{count_stars}", "")

        screen.blit(pygame.transform.scale(image,(screen.get_width(),screen.get_height())),(0,0))
        star.draw()
        for s in star_list:
            s.draw()
        if not freeze:
            follow_mous(star)
        pygame.display.update()
        clock.tick(60)