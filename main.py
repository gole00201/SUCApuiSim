import dearpygui.dearpygui as dpg
import time
import numpy as np
w, h, ch, data = dpg.load_image('./img/1_main.jpg')


dpg.create_context()
dpg.create_viewport(title='BSRPI "KODER"', width=w+500, height=h-240, max_width=w+ 600, max_height=h, resizable=False)
MODE:str = 'lb'


with dpg.texture_registry(show=False):
    w, h, ch, data = dpg.load_image('./img/1_main.jpg')
    main = dpg.add_static_texture(
        width=w, height=h, default_value=data, tag='img')

    w_t, h_t, ch, data_t = dpg.load_image('./img/sprites_tmp.jpg')
    tmb_c = dpg.add_static_texture(
        width=w_t, height=h_t, default_value=data_t, tag='tmb')

    w_t, h_t, ch, data_t_off = dpg.load_image('./img/sprites_tmp_off.jpg')
    tmb_off_c = dpg.add_static_texture(
        width=w_t, height=h_t, default_value=data_t_off, tag='tmb_off')

    w_l, h_l, ch, data_l = dpg.load_image('./img/sprites_led.jpg')
    led = dpg.add_static_texture(
        width=w_l, height=h_l, default_value=data_l, tag='led')

    w_l, h_l, ch, data_l_on = dpg.load_image('./img/sprites_led_on.jpg')
    led_on = dpg.add_static_texture(
        width=w_l, height=h_l, default_value=data_l_on, tag='led_on')
    w_logo, h_logo, ch, data_logo = dpg.load_image('./img/logo.png') 
    logo = dpg.add_static_texture(width= w_logo, height= h_logo, default_value= data_logo, tag = 'logo')

    w_tmb_l, h_tmb_l, ch, data_tmb_l = dpg.load_image('./img/tmb_logo.jpg')
    tmb_logo = dpg.add_static_texture(width= w_tmb_l, height= h_tmb_l, default_value= data_tmb_l, tag = 'tmb_logo')

    w_tmb_l_1, h_tmb_l_1, ch, data_tmb_l_1 = dpg.load_image('./img/tmb_logo_1.jpg')
    tmb_logo_1 = dpg.add_static_texture(width= w_tmb_l_1, height= h_tmb_l_1, default_value= data_tmb_l_1, tag = 'tmb_logo_1')


    w_cab_t, h_cab_tmb, ch, data_cab_tmb = dpg.load_image('./img/sprites_tmp_cab.jpg')
    tmb = dpg.add_static_texture(width= w_cab_t, height= h_cab_tmb, default_value= data_cab_tmb, tag = 'tmb_c_off')
    
    w_cab_t, h_cab_tmb, ch, data_cab_tmb = dpg.load_image('./img/sprites_tmp_cab_on.jpg')
    tmb_off = dpg.add_static_texture(width= w_cab_t, height= h_cab_tmb, default_value= data_cab_tmb, tag = 'tmb_c')
    
    

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
    with dpg.font('./fonts/Cousine-Regular.ttf', 20, tag = 'menu_f'):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    with dpg.font('./fonts/Cousine-Regular.ttf', 15, tag = 'menu_f_1'):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

# Координаты для тумблеров включения и текста

tmbs_start_coord = (830, 80)
text_coords = (430, 120)

# Магия чисел с координатами следующих тумблеров (К начальной координате добовляем координату одного тумблера)
coord_tmb_lst = {'pit_tmb': tmbs_start_coord, 'sam1_tmb': (tmbs_start_coord[0], tmbs_start_coord[1] + h_cab_tmb),
                 'sil1_tmb': (tmbs_start_coord[0] + (w_cab_t + 92)*2, tmbs_start_coord[1]), 'sam2_tmb': (tmbs_start_coord[0] + (w_cab_t + 92)*2, tmbs_start_coord[1] + h_cab_tmb),
                 'sil2_tmb': (tmbs_start_coord[0] + (w_cab_t-20) * 4, tmbs_start_coord[1]+50)}
tmb_size = (w_cab_t-25, h_cab_tmb-45)

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


def draw_cntr_tmb(name: str, tmb_s: int | str=tmb_c) -> None:
    dpg.delete_item(name)
    dpg.draw_image(tmb_s, (565, 450), (w_t+545, h_t+430), uv_min=(0, 0),
                   uv_max=(1.0, 1.0), parent='sprites_drawlist', tag=name)

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
        dpg.draw_image(led_on, (210, 310), (w_l+120, h_l+295), uv_min=(0, 0),
                       uv_max=(1, 1), parent='sprites_drawlist', tag='led_img')
        dpg.set_value('pui_status', value=True)
    else:
        dpg.delete_item('led_img')
        dpg.draw_image(led, (210, 310), (w_l+120, h_l+295), uv_min=(0, 0),
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
    if dpg.does_item_exist('input_s'):
        dpg.delete_item('input_s')
    if dpg.does_item_exist('input_a'):
        dpg.delete_item('input_a')
    if dpg.get_value('pui_status'):
        global counter_main, counter_sub, counter_as, counter
        counter += 1
        if counter >= len(list_menu[dpg.get_value('in_pr')]):
            counter = 0
        # print(counter)
        draw_text(list_menu[dpg.get_value('in_pr')][counter])


def dwn_arrow():
    if dpg.does_item_exist('input_s'):
        dpg.delete_item('input_s')
    if dpg.does_item_exist('input_a'):
        dpg.delete_item('input_a')
    if dpg.get_value('pui_status'):
        global counter_main, counter_sub, counter_as, counter
        if counter == 0:
            counter = len(list_menu[dpg.get_value('in_pr')]) - 1 
        else:
            counter = counter - 1
        draw_text(list_menu[dpg.get_value('in_pr')][counter])
    
def show_alt_data() -> None:
    if dpg.does_item_exist('input_s'):
        dpg.delete_item('input_s')
    if not dpg.does_item_exist('input_a'):
        with dpg.window(no_resize= True, no_background= True, no_close=True, no_title_bar= True, no_collapse= True, pos = (730, 360), autosize= True, tag = 'input_a'):
            with dpg.group(horizontal= True, horizontal_spacing= 40):
                dpg.add_text(default_value='Введите значение высоты', tag = 'alt_t')
                dpg.add_listbox(items= alt_list, tag = 'list_alt', width= 150, callback= show_alt_data)
        dpg.bind_item_font('list_alt', 'menu_f')
        dpg.bind_item_font('alt_t', 'menu_f')
    if dpg.get_value('pui_status') and counter == 20:
        if dpg.get_value('list_alt') == '5000':
            draw_text('АС45      40\n0.790В      ')
        if dpg.get_value('list_alt') == '4000':
            draw_text('АС45      60\n1.180В      ')
        if dpg.get_value('list_alt') == '3000':
            draw_text('АС45      81\n1.590В      ')
        if dpg.get_value('list_alt') == '2000':
            draw_text('АС45      А2\n1.990В      ')
        if dpg.get_value('list_alt') == '1000':
            draw_text('АС45      С4\n2.410В      ')
        if dpg.get_value('list_alt') == '50':
            draw_text('АС45      E2\n2.780В      ')
        
def show_speed_data() -> None:
    if dpg.does_item_exist('input_a'):
        dpg.delete_item('input_a')
    if not dpg.does_item_exist('input_s'):
        with dpg.window(no_resize= True, no_background= True, no_close=True, no_title_bar= True, no_collapse= True, pos = (730, 360), autosize= True, tag = 'input_s'):
            with dpg.group(horizontal= True):
                dpg.add_text(default_value='Введите значение скорости', tag = 'speed_t')            
                dpg.add_listbox(items= speed_list, tag = 'list_sp', width= 150, callback= show_speed_data)
    dpg.bind_item_font('list_sp', 'menu_f')
    dpg.bind_item_font('speed_t', 'menu_f')  
    if dpg.get_value('pui_status') and counter == 23:
        if dpg.get_value('list_sp') == '400':
            draw_text('АС48      40\n0.790В      ')
        if dpg.get_value('list_sp') == '350':
            draw_text('АС48      5A\n1.110В      ')
        if dpg.get_value('list_sp') == '300':
            draw_text('АС48      74\n1.430В      ')
        if dpg.get_value('list_sp') == '250':
            draw_text('АС48      8D\n1.730В      ')
        if dpg.get_value('list_sp') == '200':
            draw_text('АС48      A8\n2.070В      ')
        if dpg.get_value('list_sp') == '150':
            draw_text('АС48      C2\n2.390В      ')

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
    if dpg.does_item_exist('input_a'):
        dpg.delete_item('input_a')
    if dpg.does_item_exist('input_s'):
        dpg.delete_item('input_s')
    global counter_main, counter_sub, counter_as, counter
    if dpg.get_value('pui_status') and dpg.get_value('in_pr'):
        if (counter == 20 or counter == 23) and len(dpg.get_item_label('text_b_1')) > 0:
            draw_text(list_menu[dpg.get_value('in_pr')][counter])
            return
        dpg.set_value('in_pr', dpg.get_value('in_pr') - 1)
        draw_text(list_menu[dpg.get_value('in_pr')][0])
        counter = 0
    




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
        draw_cntr_tmb('contrl_tmp', tmb_s=tmb_off_c)


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


# Глобальные переменные
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

# Вызывается когда нажимаем выход
def exit_cal() -> None:
    dpg.stop_dearpygui()

# Темы по отрисовке чего бы то ни было 
with dpg.theme() as btn_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 0, 0, 0), category= dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 0, 0, 0), category= dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.5, category= dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 255, 255, 255))
        with dpg.theme_component(dpg.mvListbox):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (0,0,0,0), category= dpg.mvThemeCat_Core)
with dpg.theme() as menu_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Text, (255,255,255,255))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 255, 255, 255), category= dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 125, 125, 255), category= dpg.mvThemeCat_Core)

# Если выбрали режим обучения последовательно вызываются функции связанные с обучением
# В конце каждой функции проверяется условие для включения следующей
# Этап обучения храниться в глобальной переменной MODE
def std_mode_1() -> None:
    global MODE
    if not dpg.does_item_exist('std_w'):        
        with dpg.window(no_resize= True, no_background= True, no_close=True, no_title_bar= True, no_collapse= True, pos = (730, 510), autosize= True, tag = 'std_w', no_move= True):
            dpg.add_text(default_value= '\tПриветствуем Вас в \nтренажере системы "Кодер"!', tag = 'std_txt', pos = (150,0))
            dpg.add_text(default_value= '\tВключить выключатели: САМОЛЕТН N1, САМОЛЕТН N2, \nАЭР ПИТ, СИЛОВЫЕ N1, СИЛОВЫЕ N2 , чтобы выполнить \nвстроенный контроль системы', tag = 'std_txt_1', pos = (60,80))
            dpg.add_text(default_value= '', tag = 'std_txt_2', pos = (130,100))
    dpg.bind_item_font('std_txt', 'menu_f')
    dpg.bind_item_font('std_txt_1', 'menu_f')
    dpg.bind_item_font('std_txt_2', 'menu_f')
    if dpg.get_value('pui_status'):
        MODE = 'st_2'

def std_mode_2() -> None:
    global MODE
    current_text:str = list_menu[dpg.get_value('in_pr')][counter]
    dpg.set_value('std_txt', '\tПроисходит встроенный контроль системы «Кодер»')
    dpg.set_value('std_txt_1', '\tЕсли система исправна, то единичные индикаторы БРПИ, \nЗБН, ПУИ, РЕГИСТРАЦИЯ под общим названием ИСПРАВНОСТЬ \nдолжны светиться, единичный индикатор ОТКАЗ \nКОДЕР не должен светиться, а на экране загорается \nфраза КОДЕР ГОТОВ.')
    dpg.set_value('std_txt_2', '\tДалее произвести градуировку системы «Кодер»\nНажатием кнопок, обозначеных стрелками, выбрать группу \nПАРАМЕТРЫ АС (параметры аналоговых сигналов). \nДля выбора нужной группы нажать кнопку ВВОД.')
    dpg.set_item_pos('std_txt', (10, 0))
    dpg.set_item_pos('std_txt_1', (10, 20))
    dpg.set_item_pos('std_txt_2', (10, 118))
    if current_text == "AC\n1-24":
        MODE = 'st_3'
        
def std_mode_3() -> None:
    global MODE
    dpg.set_value('std_txt', '\tВыбрать группу параметров АС 25-48 нажатием кнопки \n\t\t\t\t\t\tВВОД')
    dpg.set_value('std_txt_1', '')
    dpg.set_value('std_txt_2', '')
    dpg.set_item_pos('std_txt', (10, 0))
    current_text:str = list_menu[dpg.get_value('in_pr')][counter]
    if current_text == "АС25":
        MODE = 'st_4'

def std_mode_4() -> None:
    global MODE
    dpg.set_value('std_txt', '\tДля градуировки параметра высоты выбрать необходимый \nканал , то есть  АС 45, нажатием кнопки ВВОД')
    dpg.set_value('std_txt_1', '')
    dpg.set_value('std_txt_2', '')
    dpg.set_item_pos('std_txt', (10, 0))
    if counter == 20 and len(dpg.get_item_label('text_b_1')) > 0:
        MODE = 'st_5'



alt_list:list[str] = ['5000', '4000', '3000', '2000', '1000', '50']
def std_mode_5() -> None:
    global MODE
    dpg.set_value('std_txt', 'Подать поочередно \nзначения высоты из меню \n"ВВОД ПАРАМЕТРОВ" и на \nоснове данных, выдаваемых \nсистемой «Кодер» заполнить \nградуировочную таблицу и \nпостроить градуировочный \nграфик.Для возврата назад \nнажать кнопку ОТМЕНА"')
    dpg.set_item_pos('std_txt', (330, 0))
    if not dpg.does_item_exist('i_0'):
        with dpg.group(horizontal= False, pos= (3,0), parent='std_w', tag = 'tb_1'):
            with dpg.group(horizontal= True):
                dpg.add_text(default_value=  'ВЫСОТА', tag = 'i_1')
                dpg.add_text(default_value=  'НАПРЯЖ', tag = 'i_14')
                dpg.add_text(default_value=  'ПРЯМ.ХОД', tag = 'i_0')
                dpg.add_text(default_value=  ' ОБР.ХОД', tag = 'i_21')
                dpg.add_text(default_value=  ' СР.ЗНАЧ', tag = 'i_22')
            with dpg.group(horizontal= True, horizontal_spacing= 35):
                dpg.add_text(default_value=  '5000', tag = 'i_3')
                dpg.add_text(default_value=  '0,79', tag = 'i_15')
                dpg.add_text(default_value=  '  40 ', tag = 'i_2')
                dpg.add_text(default_value=  '39 ', tag = 'i_23')
                dpg.add_text(default_value=  '39.5', tag = 'i_24')
                # dpg.add_text(default_value= "")
            with dpg.group(horizontal= True, horizontal_spacing= 35):
                dpg.add_text(default_value=  '4000', tag = 'i_5')
                dpg.add_text(default_value=  '1,18', tag = 'i_16')
                dpg.add_text(default_value=  '  60 ', tag = 'i_4')
                dpg.add_text(default_value=  '59 ', tag = 'i_25')
                dpg.add_text(default_value=  '59,5', tag = 'i_26')
            with dpg.group(horizontal= True, horizontal_spacing= 35):
                dpg.add_text(default_value=  '3000', tag = 'i_7')
                dpg.add_text(default_value=  '1,59', tag = 'i_17')
                dpg.add_text(default_value=  '  81 ', tag = 'i_6')
                dpg.add_text(default_value=  '80 ', tag = 'i_27')
                dpg.add_text(default_value=  '80,5', tag = 'i_28')
                # dpg.add_text(default_value="")
            with dpg.group(horizontal= True, horizontal_spacing= 35):
                dpg.add_text(default_value=  '2000', tag = 'i_9')
                dpg.add_text(default_value=  '1,99', tag = 'i_18')
                dpg.add_text(default_value=  '  А2 ', tag = 'i_8')
                dpg.add_text(default_value=  'A2 ', tag = 'i_29')
                dpg.add_text(default_value=  'A2 ', tag = 'i_30')
                # dpg.add_text(default_value="")
            with dpg.group(horizontal= True, horizontal_spacing= 35):
                dpg.add_text(default_value=  '1000', tag = 'i_11')
                dpg.add_text(default_value=  '2,41', tag = 'i_19')
                dpg.add_text(default_value=  '  С4 ', tag = 'i_10')
                dpg.add_text(default_value=  'C4 ', tag = 'i_31')
                dpg.add_text(default_value=  'C4 ', tag = 'i_32')
                # dpg.add_text(default_value="")
            with dpg.group(horizontal= True, horizontal_spacing= 35):
                dpg.add_text(default_value=  '50  ', tag = 'i_13')
                dpg.add_text(default_value=  '2,78', tag = 'i_20')
                dpg.add_text(default_value=  '  Е2 ', tag = 'i_12')
                dpg.add_text(default_value=  'E2 ', tag = 'i_33')
                dpg.add_text(default_value=  'E2 ', tag = 'i_34')
                # dpg.add_text(default_value="")
        for i in range(35):
            dpg.bind_item_font(f'i_{i}', 'menu_f_1')
    dpg.set_value('std_txt_1', '')
    dpg.set_value('std_txt_2', '')
    if (not dpg.does_item_exist('list_alt')) and counter == 20 and len(dpg.get_item_label('text_b_1')) == 0:
        MODE = 'st_6'

def std_mode_6() -> None:
    global MODE
    if dpg.does_item_exist('tb_1'):
        dpg.delete_item('tb_1')
    dpg.set_value('std_txt', '\tДля градуировки скорости выбрать необходимый номер \nдатчика, то есть АС 48, нажатием кнопки ВВОД')
    dpg.set_value('std_txt_1', '')
    dpg.set_item_pos('std_txt', (10, 0))
    if counter == 23 and len(dpg.get_item_label('text_b_1')) > 0:
        MODE = 'st_7'

def std_mode_7() -> None:
    global MODE
    dpg.set_value('std_txt', 'Подать поочередно \nзначения скорости из меню \n"ВВОД ПАРАМЕТРОВ"и на \nоснове данных, выдаваемых \nсистемой «Кодер» заполнить \nградуировочную таблицу и \n построить градуировочный \nграфик.Для возврата назад \nнажать кнопку ОТМЕНА"')
    dpg.set_item_pos('std_txt', (335, 0))
    if not dpg.does_item_exist('i_0'):
        with dpg.group(horizontal= False, pos= (3,0), parent='std_w', tag = 'tb_1'):
            with dpg.group(horizontal= True):
                dpg.add_text(default_value=  'СКОРОСТЬ', tag = 'i_1')
                dpg.add_text(default_value=  'НАПРЯЖ', tag = 'i_14')
                dpg.add_text(default_value=  'ПРЯМ.ХОД', tag = 'i_0')
                dpg.add_text(default_value=  ' ОБР.ХОД', tag = 'i_21')
                dpg.add_text(default_value=  'СР.ЗНАЧ', tag = 'i_22')
            with dpg.group(horizontal= True, horizontal_spacing= 35):
                dpg.add_text(default_value=  '400 ', tag = 'i_3')
                dpg.add_text(default_value=  '  0,79', tag = 'i_15')
                dpg.add_text(default_value=  '  40', tag = 'i_2')
                dpg.add_text(default_value=  '39 ', tag = 'i_23')
                dpg.add_text(default_value=  '39.5', tag = 'i_24')
                # dpg.add_text(default_value= "")
            with dpg.group(horizontal= True, horizontal_spacing= 35):
                dpg.add_text(default_value=  '350 ', tag = 'i_5')
                dpg.add_text(default_value=  '  1,11', tag = 'i_16')
                dpg.add_text(default_value=  '  5A', tag = 'i_4')
                dpg.add_text(default_value=  '5A ', tag = 'i_25')
                dpg.add_text(default_value=  '5A ', tag = 'i_26')
            with dpg.group(horizontal= True, horizontal_spacing= 35):
                dpg.add_text(default_value=  '300 ', tag = 'i_7')
                dpg.add_text(default_value=  '  1,43', tag = 'i_17')
                dpg.add_text(default_value=  '  74', tag = 'i_6')
                dpg.add_text(default_value=  '73 ', tag = 'i_27')
                dpg.add_text(default_value=  '73.5', tag = 'i_28')
                # dpg.add_text(default_value="")
            with dpg.group(horizontal= True, horizontal_spacing= 35):
                dpg.add_text(default_value=  '250 ', tag = 'i_9')
                dpg.add_text(default_value=  '  1,73', tag = 'i_18')
                dpg.add_text(default_value=  '  8D', tag = 'i_8')
                dpg.add_text(default_value=  '8D ', tag = 'i_29')
                dpg.add_text(default_value=  '8D ', tag = 'i_30')
                # dpg.add_text(default_value="")
            with dpg.group(horizontal= True, horizontal_spacing= 35):
                dpg.add_text(default_value=  '200 ', tag = 'i_11')
                dpg.add_text(default_value=  '  2.07', tag = 'i_19')
                dpg.add_text(default_value=  '  A8', tag = 'i_10')
                dpg.add_text(default_value=  'A8 ', tag = 'i_31')
                dpg.add_text(default_value=  'A8 ', tag = 'i_32')
                # dpg.add_text(default_value="")
            with dpg.group(horizontal= True, horizontal_spacing= 35):
                dpg.add_text(default_value=  '150 ', tag = 'i_13')
                dpg.add_text(default_value=  '  2,39', tag = 'i_20')
                dpg.add_text(default_value=  '  C2', tag = 'i_12')
                dpg.add_text(default_value=  'C2 ', tag = 'i_33')
                dpg.add_text(default_value=  'C2 ', tag = 'i_34')
                # dpg.add_text(default_value="")
        for i in range(35):
            dpg.bind_item_font(f'i_{i}', 'menu_f_1')
    dpg.set_value('std_txt_1', '')
    dpg.set_value('std_txt_2', '')
    if (not dpg.does_item_exist('list_alt')) and counter == 23 and len(dpg.get_item_label('text_b_1')) == 0:
        MODE = 'st_8'

def std_mode_8() -> None:
    global MODE
    if dpg.does_item_exist('tb_1'):
        dpg.delete_item('tb_1')
    dpg.set_value('std_txt', '\tВстроенный контроль и градуировка системы «Кодер» \nпроизведена, выключить систему.\n\tОпробуйте свои знания в режиме "КОНТРОЛЬ".\nДля этого нажмите "ВЫБОР РЕЖИМА" -> КОНТРОЛЬ')
    dpg.set_value('std_txt_1', '')
    dpg.set_item_pos('std_txt', (10, 0))
    MODE = 'fin'


def close_warn_w() -> None:
    global MODE 
    if dpg.does_item_exist('tr_w'):
        dpg.delete_item('tr_w')
    MODE = 'tr_1'


# Контроль. Если нажимаем "контроль", то в переменную MODE помещается значение 'tr_0'.
# По такому же принципу, как и в обучении, это значение будет меняться в зависимости от этапа тренировки
def show_warn_w() -> None:
    global MODE
    if not dpg.does_item_exist('tr_w'):
        with dpg.window(width= w + 500, height= h - 200, tag = 'tr_w', no_close= True, no_collapse=True, no_title_bar= True, pos = (0,0)):
            dpg.add_text(default_value='\t\t\tСейчас Вам будет необходимо произвести процесс градуировки системы "Кодер". \nВ конце Вы увидите вашу оценку. Учитывается: время выполнения, количество неправильных действий.', pos = (190, 300))
            dpg.bind_item_font(dpg.last_item(), 'menu_f')
            dpg.add_button(label='ПРИСТУПИТЬ', pos = (550, 400), callback=close_warn_w)
            dpg.bind_item_font(dpg.last_item(), 'cab_font')
            dpg.bind_item_theme(dpg.last_item(), menu_theme)


s_t:float = 0
def train_1() -> None:
    global MODE, s_t
    s_t = time.time()
    if not dpg.does_item_exist('std_w'):        
        with dpg.window(no_resize= True, no_background= True, no_close=True, no_title_bar= True, no_collapse= True, pos = (710, 510), autosize= True, tag = 'std_w', no_move= True):
            dpg.add_text(default_value= '', tag = 'std_txt', pos = (150,0))
            dpg.add_text(default_value= '', tag = 'std_txt_1', pos = (60,80))
            dpg.add_text(default_value= '', tag = 'std_txt_2', pos = (130,100))
    if dpg.get_value('pui_status'):
        MODE = 'tr_2'   


def train_2() -> None:
    global MODE
    current_text:str = list_menu[dpg.get_value('in_pr')][counter]
    if current_text == "AC\n1-24":
        MODE = 'tr_3'

         
def train_3() -> None:
    global MODE
    current_text:str = list_menu[dpg.get_value('in_pr')][counter]
    if current_text == "АС25":
        MODE = 'tr_4'


def train_4() -> None:
    global MODE
    if counter == 20 and len(dpg.get_item_label('text_b_1')) > 0:
        MODE = 'tr_5'


table_header:list[str] = ['Высота', 'Напряжение', 'Прям.ход', 'Обр. ход', 'Ср. знач']
def train_5() -> None:
    global MODE
    if dpg.does_item_exist('cab_an'):
        dpg.delete_item('cab_an')
    dpg.draw_text(pos=(935, 455), text= 'ПОДСКАЗКИ', size = 30, tag = 'cab_an', parent= 'sprites_drawlist')
    if not dpg.does_item_exist('tb_1'):
        with dpg.table(parent= 'std_w', tag = 'tb_1', pos = (0,0), header_row= False, borders_outerH=True, borders_outerV=True, borders_innerH=True, borders_innerV=True):
            dpg.add_table_column(label= 'Высота', tag = 'h_1')
            dpg.add_table_column(label= 'Напряжение', tag = 'h_2')
            dpg.add_table_column(label= 'Код', tag = 'h_3')
            dpg.add_table_column(label= 'Обр. код', tag = 'h_4')            
            dpg.add_table_column(label= 'Ср. значение', tag = 'h_5')      
            with dpg.table_row():
                for i in range(0,5):
                    dpg.add_text(default_value=table_header[i])
                    dpg.bind_item_font(dpg.last_item(), 'menu_f')
            for i in range(0, 5):
                with dpg.table_row():
                    for j in range(0, 5):
                        dpg.add_text('          ')
                        dpg.bind_item_font(dpg.last_item(), 'menu_f')
        dpg.bind_item_font('cab_an', 'cab_font')
    if (not dpg.does_item_exist('list_alt')) and counter == 20 and len(dpg.get_item_label('text_b_1')) == 0:
        MODE = 'tr_6'


def train_6() -> None:
    global MODE
    if dpg.does_item_exist('tb_1'):
        dpg.delete_item('tb_1')
    if counter == 23 and len(dpg.get_item_label('text_b_1')) > 0:
        MODE = 'tr_7'


table_header:list[str] = ['Скорость', 'Напряжение', 'Прям.ход', 'Обр. ход', 'Ср. знач']
def train_7() -> None:
    global MODE
    if dpg.does_item_exist('cab_an'):
        dpg.delete_item('cab_an')
    dpg.draw_text(pos=(930, 455), text= 'ПОДСКАЗКИ', size = 30, tag = 'cab_an', parent= 'sprites_drawlist')
    if not dpg.does_item_exist('tb_1'):
        with dpg.table(parent= 'std_w', tag = 'tb_1', pos = (0,0), header_row= False, borders_outerH=True, borders_outerV=True, borders_innerH=True, borders_innerV=True):
            dpg.add_table_column(label= 'Высота', tag = 'h_1')
            dpg.add_table_column(label= 'Напряжение', tag = 'h_2')
            dpg.add_table_column(label= 'Код', tag = 'h_3')
            dpg.add_table_column(label= 'Обр. код', tag = 'h_4')            
            dpg.add_table_column(label= 'Ср. значение', tag = 'h_5')      
            with dpg.table_row():
                for i in range(0,5):
                    dpg.add_text(default_value=table_header[i])
                    dpg.bind_item_font(dpg.last_item(), 'menu_f')
            for i in range(0, 5):
                with dpg.table_row():
                    for j in range(0, 5):
                        dpg.add_text('          ')
                        dpg.bind_item_font(dpg.last_item(), 'menu_f')
        dpg.bind_item_font('cab_an', 'cab_font')
    if (not dpg.does_item_exist('list_alt')) and counter == 23 and len(dpg.get_item_label('text_b_1')) == 0:
        MODE = 'tr_8'
def train_8() -> None:
    global MODE, s_t
    if dpg.does_item_exist('cab_an'):
        dpg.delete_item('cab_an')
    if dpg.does_item_exist('tb_1'):
        dpg.delete_item('tb_1')
    MODE = 'fin'
    tr_time = time.time() - s_t
    dpg.draw_text(pos=(895, 455), text= 'ВАШ РЕЗУЛЬТАТ', size = 30, tag = 'cab_an', parent = 'sprites_drawlist')
    if tr_time < 140:
        dpg.draw_text(pos=(945, 500), text= 'ОТЛИЧНО', size = 30, tag = 'cab_an_1', parent = 'sprites_drawlist')
    if 140 < tr_time and tr_time <= 160:
        dpg.draw_text(pos=(955, 500), text= 'ХОРОШО', size = 30, tag = 'cab_an_12', parent = 'sprites_drawlist')
    if 160 < tr_time and tr_time <= 180:
        dpg.draw_text(pos=(885, 500), text= 'УДОВЛЕТВОРИТЕЛЬНО', size = 30, tag = 'cab_an_13', parent = 'sprites_drawlist')
    if 180 < tr_time:
        dpg.draw_text(pos=(870, 500), text= 'НЕУДОВЛЕТВОРИТЕЛЬНО', size = 30, tag = 'cab_an_14', parent = 'sprites_drawlist')
    dpg.bind_item_font('cab_an', 'cab_font')


# Функция отрисовки главного окна как для тренировки, так для обучения
speed_list:list[str] = ['400', '350', '300', '250', '200', '150']
def train_or_study_call(s:str, a_d:str , u_d:str) -> None:
    global MODE
    MODE = u_d
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
        dpg.draw_image(main, (0, 0), (w- 140, h- 165), uv_min=(
            0, 0), uv_max=(1, 1), tag='show_img')
        dpg.draw_image(tmb_logo_1, (800, 90), (w_tmb_l + 760, h_tmb_l+10), uv_min= (0,0), uv_max = (1, 1), tag = 'show_tmb_logo_1')
        dpg.draw_image(tmb_logo, (1100, 90), (w_tmb_l + 1060, h_tmb_l+10), uv_min= (0,0), uv_max = (1, 1), tag = 'show_tmb_logo')
        draw_tmb('pit_tmb')
        draw_tmb('sam1_tmb')
        draw_tmb('sil1_tmb')
        draw_tmb('sam2_tmb')
        draw_tmb('sil2_tmb')
        dpg.draw_image(tmb_c, (565, 450), (w_t+545, h_t+430),
                    uv_min=(0, 0), uv_max=(1, 1), tag='contrl_tmb')
        dpg.draw_image(led, (210, 310), (w_l+120, h_l+295),
                    uv_min=(0, 0), uv_max=(1, 1), tag='led_img')
        dpg.draw_text(pos=(950, 60), text = 'КАБИНА', size= 30, color=(255, 255, 255, 255), tag = 'cab')
        dpg.draw_text(pos=(925, 300), text= '   ВВОД\nПАРАМЕТРОВ', size = 30, tag = 'cab_par')
        dpg.draw_text(pos=(930, 455), text= 'ПОДСКАЗКИ', size = 30, tag = 'cab_an')
        dpg.draw_text(pos =(list(coord_tmb_lst.values())[0][0] + 150, list(coord_tmb_lst.values())[0][1]+ 150) , text = 'АЭР\nПИТ', size = 30, tag = f'tmb{0}')
        dpg.draw_line(p1 = (w-150, 0), p2 = (w-150, h - 165), thickness= 20)
    if dpg.does_item_exist('st_w'):
        dpg.delete_item('st_w')
    with dpg.window(width=w + 600, height=h-165, no_background=True, pos=[0, 0], no_move=True, no_resize=True, no_title_bar= True, no_bring_to_front_on_focus=True, tag ='st_w'):
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
        # dpg.add_button(width=60, height=60, pos=[85, 4s30])
        dpg.add_button(callback=contr_tmp, width=60, height=60, pos=[575, 460])
        dpg.add_button(callback=dwn_arrow, width=60, height=60, pos=[390, 560])
        dpg.add_button(callback=up_arrow, width=60, height=60, pos=[260, 560])
        dpg.add_button(callback= out_, width=60, height=60, pos=[120, 560])
        dpg.add_button(callback= in_, width=60, height=60, pos=[535, 560])
        with dpg.window(tag='text_w', no_background= True, no_close=True, no_collapse= True, no_move= True, no_resize= True, no_title_bar= True, min_size= (200, 200), pos= (150, 93)):  
            dpg.add_button(label= 'text', tag = 'text_b', width= 400)
            dpg.add_button(label= '', tag= 'text_b_1', width= 400)
        draw_text()
    dpg.bind_item_font('cab_par', 'cab_font')
    dpg.bind_item_font('cho_mode', 'menu_f')
    dpg.bind_item_font('exit_b', 'menu_f')
    dpg.bind_item_font('cab', 'cab_font')
    dpg.bind_theme(btn_theme)
    dpg.bind_item_theme('cho_mode', menu_theme)
    dpg.bind_item_theme('exit_b', menu_theme)



# Функция отрисовки окна с выбором режимов
def lable_w() -> None:
    global MODE
    if dpg.does_item_exist('input_s'):
        dpg.delete_item('input_s')
    if dpg.does_item_exist('input_a'):
        dpg.delete_item('input_a')
    MODE = 'lb'
    if dpg.does_item_exist('text_w'):
        dpg.delete_item('text_w')
    with dpg.window(width= w+500, height=h-165, pos = (0, 0), no_title_bar= True, tag = 'lable_w'):
        dpg.add_text(pos = (w - 200, 100), default_value="Компьютерный тренажер \n   системы 'Кодер'", tag = 'lable_text')
        with dpg.viewport_drawlist(front= True, tag = 'lable_logo'):
            dpg.draw_image(logo, (580, 200), (w_logo + 90,h_logo - 120), uv_min=(0,0), uv_max= (1,1), tag = 'logo_img')
        dpg.add_button(label= "Обучение", pos = (240, 250), callback= train_or_study_call,user_data= 'st_1' ,tag = 'st_mode_act')
        dpg.add_button(label= "Контроль", pos = (240, 350), callback = train_or_study_call, user_data='tr_0', tag = 'contrl_mode_act')
        dpg.add_button(label= "Выход", pos = (280, 450), callback = exit_cal, tag = 'exit_act')
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
while dpg.is_dearpygui_running():
    # Пока мы обрабатываем графику, проверяем состояние переменной MODE и вызываем функцию этапа обучения/контроля
    if MODE == 'st_1':
        std_mode_1()
    if MODE == 'st_2':
        std_mode_2()
    if MODE == 'st_3':
        std_mode_3()
    if MODE == 'st_4':
        std_mode_4()
    if MODE == 'st_5':
        std_mode_5()
    if MODE == 'st_6':
        std_mode_6()
    if MODE == 'st_7':
        std_mode_7()
    if MODE == 'st_8':
        std_mode_8()
    if MODE == 'tr_0':
        show_warn_w()
    if MODE == 'tr_1':
        train_1()
    if MODE == 'tr_2':
        train_2()
    if MODE == 'tr_3':
        train_3()
    if MODE == 'tr_4':
        train_4()
    if MODE == 'tr_5':
        train_5()
    if MODE == 'tr_6':
        train_6()
    if MODE == 'tr_7':
        train_7()
    if MODE == 'tr_8':
        train_8()
    if MODE == 'lb':
        if dpg.does_item_exist('std_w'):
            dpg.delete_item('std_w')
    dpg.render_dearpygui_frame()
dpg.destroy_context()
