import datetime
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle

CHINESE_FONT = 'chinese.ttf'

# 完整時間表數據
NR762_TO_SIU_HONG = ["06:15", "06:30", "06:45", "07:00", "07:15", "07:30", "07:45", "08:00", "08:15", "08:30", "08:45", "09:00", "10:05", "10:20", "10:40", "11:00", "11:20", "11:40", "12:00", "14:05", "14:20", "14:40", "15:00", "15:20", "15:40", "16:00", "18:15", "18:30", "18:45", "19:00", "19:15", "19:30", "19:45", "21:15", "21:45", "22:00"]
NR762_FROM_SIU_HONG = ["06:20", "06:35", "06:50", "07:05", "07:20", "07:35", "07:50", "08:05", "08:20", "08:35", "08:50", "09:05", "10:10", "10:25", "10:45", "11:05", "11:25", "11:45", "12:05", "14:10", "14:25", "14:45", "15:05", "15:25", "15:45", "16:05", "18:20", "18:35", "18:50", "19:05", "19:20", "19:35", "19:50", "21:20", "22:05"]
NR762A_TO_TOWN = ["07:30", "08:00", "08:30", "09:00", "09:15", "09:30", "09:45", "10:00", "10:30", "11:00", "11:30", "12:00", "12:15", "12:30", "12:45", "13:00", "13:15", "13:30", "13:45", "14:00", "14:30", "15:00", "15:30", "16:00", "16:15", "16:30", "16:45", "17:00", "17:15", "17:30", "17:45", "18:00", "19:30", "20:00", "20:15", "20:30", "20:45", "21:00", "21:30", "22:00", "22:15", "22:30", "22:45", "23:00", "23:15"]
NR762A_FROM_TOWN = ["07:40", "08:10", "08:40", "09:10", "09:25", "09:40", "09:55", "10:10", "10:40", "11:10", "11:40", "12:10", "12:25", "12:40", "12:55", "13:10", "13:25", "13:40", "13:55", "14:10", "14:40", "15:10", "15:40", "16:10", "16:25", "16:40", "16:55", "17:10", "17:25", "17:40", "17:55", "18:10", "19:40", "20:10", "20:25", "20:40", "20:55", "21:10", "21:40", "22:10", "22:25", "22:40", "22:55", "23:10", "23:30"]

class ColoredCard(BoxLayout):
    def __init__(self, bg_color, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        self.orientation = 'vertical'
        self.padding = [25, 25, 25, 25] # 內邊距再次拉大，營造高級空氣感
        self.size_hint_y = None
        self.height = 240                # 【極致拉闊】卡片高度直接給到 240
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[16]) # 圓角稍微加大，更好看

class BusApp(App):
    def build(self):
        self.font = CHINESE_FONT if os.path.exists(CHINESE_FONT) else None
        
        main_layout = BoxLayout(orientation='vertical')
        with main_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1) 
            import kivy.graphics
            self.rect = kivy.graphics.Rectangle(pos=main_layout.pos, size=main_layout.size)
        main_layout.bind(pos=self.update_rect, size=self.update_rect)

        # 頂部標題欄
        top_bar = BoxLayout(orientation='vertical', size_hint_y=None, height=110, padding=[0, 25], spacing=8)
        with top_bar.canvas.before:
            Color(0.89, 0.31, 0.13, 1) 
            self.top_rect = kivy.graphics.Rectangle(pos=top_bar.pos, size=top_bar.size)
        top_bar.bind(pos=self.update_top_rect, size=self.update_top_rect)
        
        self.title_label = Label(text="居民巴士時間表", font_size='24sp', bold=True, font_name=self.font)
        self.sub_title = Label(text="豫豐花園 The Sherwood", font_size='14sp', font_name=self.font)
        top_bar.add_widget(self.title_label)
        top_bar.add_widget(self.sub_title)
        main_layout.add_widget(top_bar)

        # 滾動區域
        scroll_view = ScrollView(do_scroll_x=False, do_scroll_y=True)
        self.card_container = BoxLayout(orientation='vertical', padding=18, spacing=20, size_hint_y=None)
        self.card_container.bind(minimum_height=self.card_container.setter('height'))

        self.routes_config = [
            {"title": "NR762  豫豐花園 → 港鐵兆康站", "data": NR762_TO_SIU_HONG, "color": [0.89, 0.35, 0.18, 1]},
            {"title": "NR762  港鐵兆康站 → 豫豐花園", "data": NR762_FROM_SIU_HONG, "color": [0.15, 0.42, 0.88, 1]},
            {"title": "NR762A 豫豐花園 → 屯門市中心", "data": NR762A_TO_TOWN, "color": [0.08, 0.58, 0.36, 1]},
            {"title": "NR762A 屯門市中心 → 豫豐花園", "data": NR762A_FROM_TOWN, "color": [0.53, 0.24, 0.88, 1]}
        ]

        self.cards_dict = {}
        for config in self.routes_config:
            card = ColoredCard(bg_color=config["color"])
            
            # 1. 路線標題（鎖定高度）
            title_lbl = Label(
                text=config["title"], 
                font_size='18sp', 
                bold=True, 
                font_name=self.font, 
                size_hint_y=None, 
                height=35, 
                halign='left', 
                valign='middle'
            )
            title_lbl.bind(size=title_lbl.setter('text_size'))
            card.add_widget(title_lbl)
            
            # 【核心修改】加入一個固定 25 像素高的「透明隔離帶」，物理上強行把標題和時間隔開！
            card.add_widget(Widget(size_hint_y=None, height=25))
            
            # 2. 三個班次的網格佈局（鎖定總高度）
            grid = GridLayout(cols=3, spacing=15, size_hint_y=None, height=110)
            time_labels = []
            countdown_labels = []
            
            for _ in range(3):
                # 格子內部：強制設定元件高度，並加大間距
                box = BoxLayout(orientation='vertical', spacing=12)
                
                t_lbl = Label(text="--:--", font_size='28sp', bold=True, font_name=self.font, size_hint_y=None, height=40)
                c_lbl = Label(text="--", font_size='13sp', font_name=self.font, size_hint_y=None, height=25)
                
                box.add_widget(t_lbl)
                box.add_widget(c_lbl)
                grid.add_widget(box)
                time_labels.append(t_lbl)
                countdown_labels.append(c_lbl)
                
            card.add_widget(grid)
            
            # 【再次優化】在卡片最底部保留一點彈性空間
            card.add_widget(Widget(size_hint_y=None, height=10))
            
            self.card_container.add_widget(card)
            self.cards_dict[config["title"]] = {"data": config["data"], "time_lbls": time_labels, "count_lbls": countdown_labels}

        scroll_view.add_widget(self.card_container)
        main_layout.add_widget(scroll_view)

        Clock.schedule_interval(self.update_ui, 1)
        return main_layout

    def update_rect(self, instance, value): self.rect.pos = instance.pos; self.rect.size = instance.size
    def update_top_rect(self, instance, value): self.top_rect.pos = instance.pos; self.top_rect.size = instance.size

    def calculate_countdown(self, time_str, now):
        bus_hour, bus_minute = map(int, time_str.split(':'))
        bus_time = now.replace(hour=bus_hour, minute=bus_minute, second=0, microsecond=0)
        
        if bus_time > now:
            delta = bus_time - now
            total_seconds = int(delta.total_seconds())
            
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            
            if hours > 0:
                return f"{hours}小時 {minutes}分鐘後"
            elif minutes > 0:
                return f"{minutes}分鐘 {seconds}秒後"
            else:
                return f"{seconds}秒後"
        return None

    def update_ui(self, dt):
        now = datetime.datetime.now()
        
        for title, info in self.cards_dict.items():
            upcoming_buses = []
            
            for time_str in info["data"]:
                countdown_str = self.calculate_countdown(time_str, now)
                if countdown_str:
                    upcoming_buses.append((time_str, countdown_str))
                    if len(upcoming_buses) == 3:
                        break
            
            for i in range(3):
                if i < len(upcoming_buses):
                    info["time_lbls"][i].text = upcoming_buses[i][0]
                    info["count_lbls"][i].text = upcoming_buses[i][1]
                else:
                    info["time_lbls"][i].text = "--:--"
                    info["count_lbls"][i].text = "無班次" if i == 0 and not upcoming_buses else ""

if __name__ == '__main__':
    BusApp().run()