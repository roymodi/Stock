
import kivy
from kivy.app import App 
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder


Builder.load_file('stockapp.kv')

class AppLayout(Widget):
    maximum = ObjectProperty(None)
    minimum = ObjectProperty(None)
    
    def click_press(self):
        current = self.ids.progress_bar.value
        current+=10
        self.ids.progress_bar.value = current
        self.ids.progress_label.text = f'{str(current)}%'

        maximum = self.maximum.text
        minimum = self.minimum.text
        stocklist = self.ids.spinner_id_stock_list.text
        dayrange = self.ids.spinner_id_range.text
        radio_day = self.ids.day.active
        radio_trade = self.ids.trade.active
        print(maximum,minimum,stocklist,dayrange,radio_day,radio_trade)
        

class StockApp(App):
    def build(self):
        return AppLayout()

if __name__ == "__main__":
    StockApp().run()