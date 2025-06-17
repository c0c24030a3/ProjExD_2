import os
import random
import sys
import time
import pygame as pg



WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct:pg.Rect)->tuple[bool,bool]:
    """
    引数:こうかとんRectかばくだんRect
    戻り値:タプル(横方向判定結果,縦方向判定結果)
    画面内ならTrue,画面内ならFalse
    """
    yoko,tate=True,True #画面の中を初期値に
    if rct.left<0 or WIDTH <rct.right:
        yoko=False
    if rct.top <0 or HEIGHT<rct.bottom:
        tate=False
    return yoko ,tate#結果を返す
tmr=0
def display_update():
    """
    ゲームオーバー画面を表示する
    """
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    go_img=pg.image.load("fig/8.png")
    fonto=pg.font.Font(None,80)
    txt=fonto.render("Game Over",True,(255,255,255))
    a_img=pg.Surface((WIDTH,HEIGHT))#空のsurfaceを作る
    bg_img = pg.image.load("fig/pg_bg.jpg")
    screen.blit(bg_img, [-tmr, 0])
    screen.set_alpha(50)
    pg.draw.rect(a_img, (0, 0, 0), (0, 0,WIDTH,HEIGHT))#空surfaceに四角形を描画する
    a_img.set_alpha(50)
    screen.blit(a_img,[0,0])
    screen.blit(go_img,[100,100])
    screen.blit(go_img,[300,100])
    screen.blit(txt,[550,325])
    pg.display.update()
    time.sleep(5)

def yakitori(sum_mv):
    a=yakitori.get(tuple(sum_mv)) 
    return
bb_imgs=[]
bb_accs=[a for a in range (1,11)]
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0,0,0))
        bb_imgs.append(bb_img)
    return bb_imgs,bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img=pg.Surface((20,20))#空のSurfaceを作る
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    bb_rct=bb_img.get_rect()
    bb_rct.center=random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx,vy=+5,+5
    clock = pg.time.Clock()
    tmr = 0
    DELTA={pg.K_UP:(0,-5),pg.K_DOWN:(0,5),pg.K_LEFT:(-5,0),pg.K_RIGHT:(5,0)}
    yakitori={(0,-5):pg.transform.rotozoom(kk_img,0,1.0),(5,-5):pg.transform.rotozoom(kk_img,45,1.0),(5,0):pg.transform.rotozoom(kk_img,90,1.0),(5,5):pg.transform.rotozoom(kk_img,125,1.0),(0,5):pg.transform.rotozoom(kk_img,180,1.0),(-5,5):pg.transform.rotozoom(kk_img,225,1.0),(-5,0):pg.transform.rotozoom(kk_img,270,1.0),(-5,-5):pg.transform.rotozoom(kk_img,315,1.0),(0,0):pg.transform.rotozoom(kk_img,0,1.0)}

    bb_imgs,bb_accs=init_bb_imgs()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        avx = vx*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]

        if kk_rct.colliderect(bb_rct):
            display_update()
            time.sleep(2)
            print("ゲームオーバー")
            return
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        
        for key ,mv in DELTA.items():
            if key_lst[key]:    
                sum_mv[0]+=mv[0]
                sum_mv[1]+=mv[1]
        kk_rct.move_ip(sum_mv)
        check_bound(kk_rct)
        if check_bound(kk_rct)!=(True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        sum_mv=tuple(sum_mv)
        kk_img = yakitori.get(tuple(sum_mv)) 
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(avx,vy)#爆弾の挙動
        check_bound(bb_rct)
        yoko,tate=check_bound(bb_rct)
        
        if not yoko:
            vx*=-1
        if not tate:
            vy*=-1
        
        screen.blit(bb_img, bb_rct)
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()



