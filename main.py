import dearpygui.dearpygui as dpg
import time
import numpy as np
import sys
w, h, ch, data = dpg.load_image('./img/1_main.jpg')


dpg.create_context()
dpg.create_viewport(title="Diplom", width=w+600, height=h, max_width=w+ 600, max_height=h, resizable=False)


with dpg.texture_registry(show=False):
    w, h, ch, data = dpg.load_image('./img/1_main.jpg')
    main = dpg.add_static_texture(
        width=w, height=h, default_value=data, tag='img')

    w_t, h_t, ch, data_t = dpg.load_image('./img/sprites_tmp.jpg')
    tmb = dpg.add_static_texture(
        width=w_t, height=h_t, default_value=data_t, tag='tmb')

    w_t, h_t, ch, data_t_off = dpg.load_image('./img/sprites_tmp_off.jpg')
    tmb_off = dpg.add_static_texture(
        width=w_t, height=h_t, default_value=data_t_off, tag='tmb_off')

    w_l, h_l, ch, data_l = dpg.load_image('./img/sprites_led.jpg')
    led = dpg.add_static_texture(
        width=w_l, height=h_l, default_value=data_l, tag='led')

    w_l, h_l, ch, data_l_on = dpg.load_image('./img/sprites_led_on.jpg')
    led_on = dpg.add_static_texture(
        width=w_l, height=h_l, default_value=data_l_on, tag='led_on')
    w_logo, h_logo, ch, data_logo = dpg.load_image('./img/logo.png') 
    logo = dpg.add_static_texture(width= w_logo, height= h_logo, default_value= data_logo, tag = 'logo')

list_main_menu:list[str] = ["ПАРАМЕТРЫ\nАC",
            "КОНТРОЛЬ\nПИТАНИЯ", "РК\n", "ДПК\n"]

list_sub_menu:list[str] = ["AC\n1-24", "AC\n25-48", "AC\n49", "AC\n50", 
                           "AC\n55-70", "Трез", "ТМП", "СКТ", 
                           "СЛС", "115 В", "27 В", "ПЧК", "РК"]

list_as_menu:list[str] = [f"АС{i}" for i in range(25, 49)]

list_menu:list[list[str]] = [list_main_menu, list_sub_menu, list_as_menu]


with dpg.font_registry() as main_font_reg:
    with dpg.font("./fonts/Cousine-Regular.ttf", 50, default_font=True, tag='Main_font'):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    with dpg.font('./fonts/Cousine-Bold.ttf', 50, tag = 'cab_font'):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    with dpg.font('./fonts/Cousine-Regular.ttf', 20, tag = 'cab_tmb_f'):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    with dpg.font('./fonts/Cousine-Regular.ttf', 30, tag = 'menu_f'):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

# Координаты для тумблеров включения и текста

tmbs_start_coord = (900, 180)
text_coords = (430, 120)

# Магия чисел с координатами следующих тумблеров (К начальной координате добовляем координату одного тумблера)
coord_tmb_lst = {'pit_tmb': tmbs_start_coord, 'sam1_tmb': (tmbs_start_coord[0] + w_t, tmbs_start_coord[1]),
                 'sil1_tmb': (tmbs_start_coord[0] + w_t*2, tmbs_start_coord[1]), 'sam2_tmb': (tmbs_start_coord[0] + w_t*3, tmbs_start_coord[1]),
                 'sil2_tmb': (tmbs_start_coord[0] + w_t * 4, tmbs_start_coord[1])}
tmb_size = (w_t, h_t)

# Сложить два тьюпла чтобы в draw_image можно было быстро определить pmax и pmin


def sum_tpl(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, ...]:
    return tuple(np.add(x, y))

# Сокращенная запись отрисовки тумблера


def draw_tmb(name: str, tmb_state: int | str =tmb) -> None:
    dpg.draw_image(tmb_state, tuple(coord_tmb_lst[name]), sum_tpl(tmb_size, coord_tmb_lst[name]), uv_min=(0, 0),
                   uv_max=(1, 1), parent='sprites_drawlist', tag=name)


# Отрисовка текста
def draw_text(text=""):
    if len(text.split('\n')) == 2:
        dpg.set_item_label(item= 'text_b', label= text.split('\n')[0])
        dpg.set_item_label(item= 'text_b_1', label= text.split('\n')[1])
    else:
        dpg.set_item_label(item= 'text_b', label= text)
        dpg.set_item_label(item= 'text_b_1', label='')

# Позиция другая, поэтому отрисовываем тумблер котроля отдельной функциекй


def draw_cntr_tmb(name: str, tmb_s: int | str=tmb) -> None:
    dpg.delete_item(name)
    dpg.draw_image(tmb_s, (680, 540), (w_t+680, h_t+540), uv_min=(0, 0),
                   uv_max=(1, 1), parent='sprites_drawlist', tag=name)

# Самая банальная проверка на "включенность" всех тумблеров (вызывается каждое нажатие на тумблер)


def check_tmb():
    pit = dpg.get_value('bool_pit')
    sam1 = dpg.get_value('bool_sam1')
    sil1 = dpg.get_value('bool_sil1')
    sam2 = dpg.get_value('bool_sam2')
    sil2 = dpg.get_value('bool_sil2')
    if pit and sam1 and sil1 and sam2 and sil2:
        draw_text(dpg.get_value("main_string"))
        time.sleep(1)
        dpg.delete_item('led_img')
        dpg.draw_image(led_on, (250, 380), (w_l+250, h_l+380), uv_min=(0, 0),
                       uv_max=(1, 1), parent='sprites_drawlist', tag='led_img')
        dpg.set_value('pui_status', value=True)
    else:
        dpg.delete_item('led_img')
        dpg.draw_image(led, (250, 380), (w_l+250, h_l+380), uv_min=(0, 0),
                       uv_max=(1, 1), parent='sprites_drawlist', tag='led_img')
        dpg.set_value('pui_status', value=False)
        global counter_main, counter_sub, counter_as, counter
        dpg.set_value('in_pr', 0)
        counter = 0 
        counter_main = 0
        counter_sub = 0
        counter_as = 0
        draw_text()

# Далее работа со стрелами, тоже самый банальный вариант, берем просто счетчик и сбарасываем его каждый раз как дошли до конца списка

counter:int = 0
counter_main:int = 0
counter_sub:int = 0
counter_as:int = 0
input_counter:int = 0

def up_arrow():
    if dpg.get_value('pui_status'):
        global counter_main, counter_sub, counter_as, counter
        counter += 1
        if counter >= len(list_menu[dpg.get_value('in_pr')]):
            counter = 0
        # print(counter)
        draw_text(list_menu[dpg.get_value('in_pr')][counter])


def dwn_arrow():
    if dpg.get_value('pui_status'):
        global counter_main, counter_sub, counter_as, counter
        if counter == 0:
            counter = len(list_menu[dpg.get_value('in_pr')]) - 1 
        else:
            counter = counter - 1
        draw_text(list_menu[dpg.get_value('in_pr')][counter])
        # print(counter)
 
def show_alt_data() -> None:
    if dpg.get_value('pui_status') and counter == 20:
        if dpg.get_value('list_alt') == '5000':
            draw_text('АС45      40\n4.565В      ')
        if dpg.get_value('list_alt') == '4000':
            draw_text('АС45      60\n4.575В      ')
        if dpg.get_value('list_alt') == '3000':
            draw_text('АС45      81\n4.515В      ')
        if dpg.get_value('list_alt') == '2000':
            draw_text('АС45      А2\n4.525В      ')
        if dpg.get_value('list_alt') == '1000':
            draw_text('АС45      С4\n4.595В      ')
        if dpg.get_value('list_alt') == '50':
            draw_text('АС45      E2\n4.505В      ')
        
def show_speed_data() -> None:
    if dpg.get_value('pui_status') and counter == 23:
        if dpg.get_value('list_sp') == '400':
            draw_text('АС48      40\n4.565В      ')
        if dpg.get_value('list_sp') == '350':
            draw_text('АС48      5A\n4.575В      ')
        if dpg.get_value('list_sp') == '300':
            draw_text('АС48      74\n4.515В      ')
        if dpg.get_value('list_sp') == '250':
            draw_text('АС48      8D\n4.525В      ')
        if dpg.get_value('list_sp') == '200':
            draw_text('АС48      A8\n4.595В      ')
        if dpg.get_value('list_sp') == '150':
            draw_text('АС48      C2\n4.505В      ')

def in_():
    global counter_main, counter_sub, counter_as, counter
    current_text:str = list_menu[dpg.get_value('in_pr')][counter]
    if dpg.get_value('pui_status') and (current_text == 'АС45'):
        show_alt_data()
        return
    if dpg.get_value('pui_status') and (current_text == 'АС48'):
        show_speed_data()
        return
    if dpg.get_value('in_pr')  == 3:
        return
    elif dpg.get_value('pui_status') and ( current_text == "ПАРАМЕТРЫ\nАC" or current_text == "AC\n25-48"):
        dpg.set_value('in_pr', dpg.get_value('in_pr') + 1)
        draw_text(list_menu[dpg.get_value('in_pr')][0])
        counter = 0
    else: 
        return

def out_():
    global counter_main, counter_sub, counter_as, counter
    if dpg.get_value('pui_status') and dpg.get_value('in_pr'):
        if (counter == 20 or counter == 23) and len(dpg.get_item_label('text_b_1')) > 0:
            draw_text(list_menu[dpg.get_value('in_pr')][counter])
            return
        dpg.set_value('in_pr', dpg.get_value('in_pr') - 1)
        draw_text(list_menu[dpg.get_value('in_pr')][0])
        counter = 0
    


# Колбэки для тумблеров

def contr_tmp():
    # Узнали в каком сейчас состоянии тумблер
    state = dpg.get_value('bool_contrl')
    if state:
        # Изменили это состояние
        dpg.set_value('bool_contrl', value=False)
        # Удалили старый и нарисовали новый
        draw_cntr_tmb('contrl_tmp')
    else:
        dpg.set_value('bool_contrl', value=True)
        draw_cntr_tmb('contrl_tmp', tmb_s=tmb_off)


def pit_tmb():
    dpg.delete_item('pit_tmb')
    state = dpg.get_value('bool_pit')
    if state:
        dpg.set_value('bool_pit', value=False)
        draw_tmb('pit_tmb', tmb_state=tmb)
    else:
        dpg.set_value('bool_pit', value=True)
        draw_tmb('pit_tmb', tmb_state=tmb_off)
    check_tmb()


def sam1_tmb():
    dpg.delete_item('sam1_tmb')
    state = dpg.get_value('bool_sam1')
    if state:
        dpg.set_value('bool_sam1', value=False)
        draw_tmb('sam1_tmb', tmb_state=tmb)
    else:
        dpg.set_value('bool_sam1', value=True)
        draw_tmb('sam1_tmb', tmb_state=tmb_off)
    check_tmb()


def sail_tmb():
    dpg.delete_item('sil1_tmb')
    state = dpg.get_value('bool_sil1')
    if state:
        dpg.set_value('bool_sil1', value=False)
        draw_tmb('sil1_tmb', tmb_state=tmb)
    else:
        dpg.set_value('bool_sil1', value=True)
        draw_tmb('sil1_tmb', tmb_state=tmb_off)
    check_tmb()


def sam2_tmb():
    dpg.delete_item('sam2_tmb')
    state = dpg.get_value('bool_sam2')
    if state:
        dpg.set_value('bool_sam2', value=False)
        draw_tmb('sam2_tmb', tmb_state=tmb)
    else:
        dpg.set_value('bool_sam2', value=True)
        draw_tmb('sam2_tmb', tmb_state=tmb_off)
    check_tmb()


def sil2_tmb():
    dpg.delete_item('sil2_tmb')
    state = dpg.get_value('bool_sil2')
    if state:
        dpg.set_value('bool_sil2', value=False)
        draw_tmb('sil2_tmb', tmb_state=tmb)
    else:
        dpg.set_value('bool_sil2', value=True)
        draw_tmb('sil2_tmb', tmb_state=tmb_off)
    check_tmb()

# Нужды ДПГ по отрисовке


with dpg.value_registry():
    dpg.add_bool_value(default_value=False, tag="pui_status")
    dpg.add_bool_value(default_value=False, tag="bool_contrl")
    dpg.add_bool_value(default_value=False, tag="bool_pit")
    dpg.add_bool_value(default_value=False, tag="bool_sam1")
    dpg.add_bool_value(default_value=False, tag="bool_sil1")
    dpg.add_bool_value(default_value=False, tag="bool_sam2")
    dpg.add_bool_value(default_value=False, tag="bool_sil2")
    dpg.add_int_value(default_value=0, tag="in_pr")
    dpg.add_string_value(default_value="КОДЕР\nГОТОВ", tag='main_string')


list_of_cab_tmb:list[str] = ['ПИТ', 'САМ1', 'СИЛ1', 'САМ2', 'СИЛ2']


def exit_cal() -> None:
    dpg.stop_dearpygui()


with dpg.theme() as btn_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 0, 0, 0), category= dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 0, 0, 0), category= dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.5, category= dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))
        with dpg.theme_component(dpg.mvListbox):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (0,0,0,0), category= dpg.mvThemeCat_Core)
with dpg.theme() as menu_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Text, (255,255,255,255))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 255, 255, 255), category= dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 125, 125, 255), category= dpg.mvThemeCat_Core)
        # dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.5, category= dpg.mvThemeCat_Core)
        # dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 255, 255, 255))



    

speed_list:list[str] = ['400', '350', '300', '250', '200']
alt_list:list[str] = ['5000', '4000', '3000', '2000', '1000', '50']
def study_cal() -> None:
    dpg.delete_item('lable_w')
    dpg.delete_item('lable_logo')
    dpg.delete_item('sprites_drawlist')
    dpg.set_value('pui_status', False)
    dpg.set_value('bool_contrl', False)
    dpg.set_value('bool_pit', False)
    dpg.set_value('bool_sam1', False)
    dpg.set_value('bool_sam2', False)
    dpg.set_value('bool_sil2', False)
    with dpg.viewport_drawlist(front=False, tag='sprites_drawlist'):
        dpg.draw_image(main, (0, 0), (w, h), uv_min=(
            0, 0), uv_max=(1, 1), tag='show_img')
        draw_tmb('pit_tmb')
        draw_tmb('sam1_tmb')
        draw_tmb('sil1_tmb')
        draw_tmb('sam2_tmb')
        draw_tmb('sil2_tmb')
        dpg.draw_image(tmb, (680, 540), (w_t+680, h_t+540),
                    uv_min=(0, 0), uv_max=(1, 1), tag='contrl_tmb')

        dpg.draw_image(led, (250, 380), (w_l+250, h_l+380),
                    uv_min=(0, 0), uv_max=(1, 1), tag='led_img')
        dpg.draw_text(pos=(1060, 80), text = 'КАБИНА', size= 60, color=(255, 255, 255, 255), tag = 'cab')
        dpg.draw_text(pos=(1060, 300), text= '   ВВОД\nПАРАМЕТРОВ', size = 40, tag = 'cab_par')
        i:int  = 0
        for tmb_b in list_of_cab_tmb:
            dpg.draw_text(pos =(list(coord_tmb_lst.values())[i][0] + 20, list(coord_tmb_lst.values())[i][1] - 27) , text = tmb_b, size = 30, tag = f'tmb{i}')
            i+= 1
    if dpg.does_item_exist('st_w'):
        dpg.delete_item('st_w')
    with dpg.window(width=w + 600, height=h, no_background=True, pos=[0, 0], no_move=True, no_resize=True, no_title_bar= True, no_bring_to_front_on_focus=True, tag ='st_w'):
        with dpg.menu_bar():
            dpg.add_button(label="Выбор режима", callback= lable_w, tag = 'cho_mode')
            dpg.add_button(label="Выход", callback= exit_cal, tag = 'exit_b')
        dpg.add_button(callback=pit_tmb, width=100, height=100,
                    pos=tuple(coord_tmb_lst['pit_tmb']))
        dpg.add_button(callback=sam1_tmb, width=100, height=100,
                    pos=tuple(coord_tmb_lst['sam1_tmb']))
        dpg.add_button(callback=sail_tmb, width=100, height=100,
                    pos=tuple(coord_tmb_lst['sil1_tmb']))
        dpg.add_button(callback=sam2_tmb, width=100, height=100,
                    pos=tuple(coord_tmb_lst['sam2_tmb']))
        dpg.add_button(callback=sil2_tmb, width=100, height=100,
                    pos=tuple(coord_tmb_lst['sil2_tmb']))
        dpg.add_button(width=90, height=90, pos=[85, 530])
        dpg.add_button(callback=contr_tmp, width=90, height=90, pos=[680, 540])
        dpg.add_button(callback=dwn_arrow, width=90, height=90, pos=[460, 670])
        dpg.add_button(callback=up_arrow, width=90, height=90, pos=[300, 670])
        dpg.add_button(callback= out_, width=90, height=90, pos=[140, 670])
        dpg.add_button(callback= in_, width=90, height=90, pos=[630, 670])
        with dpg.window(tag='text_w', no_background= True, no_close=True, no_collapse= True, no_move= True, no_resize= True, no_title_bar= True, min_size= (200, 200), pos= (w/2 - 200, 120)):  
            dpg.add_button(label= 'text', tag = 'text_b', width= 400)
            dpg.add_button(label= '', tag= 'text_b_1', width= 400)
        draw_text()
        with dpg.window(no_resize= True, no_background= True, no_close=True, no_title_bar= True, no_collapse= True, pos = (850, 400), autosize= True, tag = 'input_w'):
            with dpg.group(horizontal= True, horizontal_spacing= 40):
                dpg.add_text(default_value='Введите значение высоты', tag = 'alt_t')
                dpg.add_listbox(items= alt_list, tag = 'list_alt', width= 150, callback= show_alt_data)
            with dpg.group(horizontal= True):
                dpg.add_text(default_value='Введите значение скорости', tag = 'speed_t')            
                dpg.add_listbox(items= speed_list, tag = 'list_sp', width= 150, callback= show_speed_data)
    dpg.bind_item_font('list_sp', 'menu_f')
    dpg.bind_item_font('list_alt', 'menu_f')
    
    dpg.bind_item_font('cab_par', 'cab_font')
    dpg.bind_item_font('alt_t', 'menu_f')
    dpg.bind_item_font('speed_t', 'menu_f')    
    dpg.bind_item_font('cho_mode', 'menu_f')
    dpg.bind_item_font('exit_b', 'menu_f')
    dpg.bind_item_font('cab', 'cab_font')
    for i in range(len(list_of_cab_tmb)):
        dpg.bind_item_font(f'tmb{i}', 'cab_tmb_f')
    dpg.bind_theme(btn_theme)
    # dpg.bind_item_theme('list_sp', menu_theme)
    # dpg.bind_item_theme('list_alt', menu_theme)
    dpg.bind_item_theme('cho_mode', menu_theme)
    dpg.bind_item_theme('exit_b', menu_theme)


def lable_w() -> None:
    if dpg.does_item_exist('text_w'):
        dpg.delete_item('text_w')
    if dpg.does_item_exist('input_w'):
        dpg.delete_item('input_w')
    with dpg.window(width= w+600, height=h+250, pos = (0, 0), no_title_bar= True, tag = 'lable_w'):
        dpg.add_text(pos = (w - 400, 0), default_value="Компьютерный тренажер \n   системы 'Кодер'", tag = 'lable_text')
        with dpg.viewport_drawlist(front= True, tag = 'lable_logo'):
            dpg.draw_image(logo, (380, 100), (w_logo - 110,h_logo - 250), uv_min=(0,0), uv_max= (1,1), tag = 'logo_img')
        dpg.add_button(label= "Обучение", pos = (640, 600), callback= study_cal, tag = 'st_mode_act')
        dpg.add_button(label= "Контроль", pos = (640, 700), tag = 'contrl_mode_act')
        dpg.add_button(label= "Выход", pos = (680, 800), callback = exit_cal, tag = 'exit_act')
    dpg.bind_item_font('st_mode_act', 'cab_font')
    dpg.bind_item_font('contrl_mode_act', 'cab_font')
    dpg.bind_item_font('exit_act', 'cab_font')
    dpg.bind_item_theme('st_mode_act', menu_theme)    
    dpg.bind_item_theme('contrl_mode_act', menu_theme)
    dpg.bind_item_theme('exit_act', menu_theme)

lable_w()
dpg.bind_font('Main_font')


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
