from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.graphics import Color, Bezier, Line
import random

Config.set('graphics', 'resizable', '0') #0 being off 1 being on as in true/false
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '500')

Builder.load_string("""
<Boxes>:
    label00:l00
    label01:l01
    label02:l02
    label03:l03
    label04:l04
    label05:l05
    label06:l06
    label07:l07
    label08:l08
    
    label10:l10
    label11:l11
    label12:l12
    label13:l13
    label14:l14
    label15:l15
    label16:l16
    label17:l17
    label18:l18
    
    label20:l20
    label21:l21
    label22:l22
    label23:l23
    label24:l24
    label25:l25
    label26:l26
    label27:l27
    label28:l28
    
    label30:l30
    label31:l31
    label32:l32
    label33:l33
    label34:l34
    label35:l35
    label36:l36
    label37:l37
    label38:l38
    
    label40:l40
    label41:l41
    label42:l42
    label43:l43
    label44:l44
    label45:l45
    label46:l46
    label47:l47
    label48:l48
    
    label50:l50
    label51:l51
    label52:l52
    label53:l53
    label54:l54
    label55:l55
    label56:l56
    label57:l57
    label58:l58
    
    label60:l60
    label61:l61
    label62:l62
    label63:l63
    label64:l64
    label65:l65
    label66:l66
    label67:l67
    label68:l68
    
    label70:l70
    label71:l71
    label72:l72
    label73:l73
    label74:l74
    label75:l75
    label76:l76
    label77:l77
    label78:l78
    
    label80:l80
    label81:l81
    label82:l82
    label83:l83
    label84:l84
    label85:l85
    label86:l86
    label87:l87
    label88:l88

    
    AnchorLayout:
        anchor_x: 'left'
        anchor_y: 'bottom'
        ScreenManager:
            size:(500, 450)
            size_hint:(None, None) 
            id: _screen_manager
            Screen:
                name: 'screen1'
                FloatLayout:
                    Button:
                        text: "gomba"
                        size:(100, 50)
                        size_hint:(None, None) 
                        pos: (370, 300)
                        
                        on_press: root.filltable()

                GridLayout: 
                    cols: 9
                    orientation: 'vertical'
                    padding: 0
                    row_default_height: 40
                    col_default_width: 40
                    row_force_default: True
                    col_force_default: True
                    Label:
                        id:l00
                        text: "1"
                    Label:
                        id:l01
                        text: "2"
                    Label:
                        id:l02
                        text: "3"
                    Label:
                        id:l03
                        text: "4"
                    Label:
                        id:l04
                        text: "5"
                    Label:
                        id:l05
                        text: "6"
                    Label:
                        id:l06
                        text: "7"
                    Label:
                        id:l07
                        text: "8"
                    Label:
                        id:l08
                        text: "9"
                    Label:
                        id:l10                    
                        text: "1"
                    Label:
                        id:l11
                        text: "2"
                    Label:
                        id:l12
                        text: "3"
                    Label:
                        id:l13
                        text: "4"
                    Label:
                        id:l14
                        text: "5"
                    Label:
                        id:l15
                        text: "6"
                    Label:                    
                        id:l16
                        text: "7"
                    Label:
                        id:l17
                        text: "8"
                    Label:
                        id:l18
                        text: "9"
                    Label:
                        id:l20
                        text: "1"
                    Label:
                        id:l21
                        text: "2"
                    Label:
                        id:l22
                        text: "3"
                    Label:
                        id:l23
                        text: "4"
                    Label:
                        id:l24
                        text: "5"
                    Label:
                        id:l25
                        text: "6"
                    Label:
                        id:l26
                        text: "7"
                    Label:
                        id:l27
                        text: "8"
                    Label:
                        id:l28
                        text: "9"
                    Label:
                        id:l30
                        text: "1"
                    Label:
                        id:l31
                        text: "2"
                    Label:
                        id:l32
                        text: "3"
                    Label:
                        id:l33
                        text: "4"
                    Label:
                        id:l34
                        text: "5"
                    Label:
                        id:l35
                        text: "6"
                    Label:
                        id:l36
                        text: "7"
                    Label:
                        id:l37
                        text: "8"
                    Label:
                        id:l38
                        text: "9"
                    Label:
                        id:l40
                        text: "1"
                    Label:
                        id:l41
                        text: "2"
                    Label:
                        id:l42
                        text: "3"
                    Label:
                        id:l43
                        text: "4"
                    Label:
                        id:l44
                        text: "5"
                    Label:
                        id:l45
                        text: "6"
                    Label:
                        id:l46
                        text: "7"
                    Label:
                        id:l47
                        text: "8"
                    Label:
                        id:l48
                        text: "9"
                    Label:
                        id:l50
                        text: "1"
                    Label:
                        id:l51
                        text: "2"
                    Label:
                        id:l52
                        text: "3"
                    Label:
                        id:l53
                        text: "4"
                    Label:
                        id:l54
                        text: "5"
                    Label:
                        id:l55
                        text: "6"
                    Label:
                        id:l56
                        text: "7"
                    Label:
                        id:l57
                        text: "8"
                    Label:
                        id:l58
                        text: "9"
                    Label:
                        id:l60
                        text: "1"
                    Label:
                        id:l61
                        text: "2"
                    Label:
                        id:l62
                        text: "3"
                    Label:
                        id:l63
                        text: "4"
                    Label:
                        id:l64
                        text: "5"
                    Label:
                        id:l65
                        text: "6"
                    Label:
                        id:l66
                        text: "7"
                    Label:
                        id:l67
                        text: "8"
                    Label:
                        id:l68
                        text: "9"
                    Label:
                        id:l70
                        text: "1"
                    Label:
                        id:l71
                        text: "2"
                    Label:
                        id:l72
                        text: "3"
                    Label:
                        id:l73
                        text: "4"
                    Label:
                        id:l74
                        text: "5"
                    Label:
                        id:l75
                        text: "6"
                    Label:
                        id:l76
                        text: "7"
                    Label:
                        id:l77
                        text: "8"
                    Label:
                        id:l78
                        text: "9"
                    Label:
                        id:l80
                        text: "1"
                    Label:
                        id:l81
                        text: "2"
                    Label:
                        id:l82
                        text: "3"
                    Label:
                        id:l83
                        text: "4"
                    Label:
                        id:l84
                        text: "5"
                    Label:
                        id:l85
                        text: "6"
                    Label:
                        id:l86
                        text: "7"
                    Label:
                        id:l87
                        text: "8"
                    Label:
                        id:l88
                        text: "9"

                    
                    
            Screen:
                name: 'screen2'
                Label: 
                    text: 'Another Screen'
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        padding:0
        BoxLayout:
            orientation: 'horizontal'
            size:(500, 50)
            size_hint:(None, None) 
            Button:
                size:(100, 50)
                size_hint:(None, None)                
                text: 'load'
                on_press: root.loadtable()
            Button:
                size:(100, 50)
                size_hint:(None, None) 
                text: 'gomb2'
                on_press: _screen_manager.current = 'screen1'
            Button:
                size:(100, 50)
                size_hint:(None, None) 
                text: 'gomb3'
                on_press: _screen_manager.current = 'screen1'
            Button:
                size:(100, 50)
                size_hint:(None, None) 
                text: 'gomb4'
                on_press: _screen_manager.current = 'screen1'
            Button:
                text: 'Exit'
                size:(100, 50)
                size_hint:(None, None) 
                on_press: app.stop() 
                """)


class Boxes(FloatLayout):
    def filltable(self):
        for col in range(9):
            for row in range(9):
                command=("self.label"+str(row)+str(col)+".text = \"" + str(random.randint(0,9)) + "\"")
                exec(command)


    def loadtable(self):
        input="1.95.67....5....26...2.3..5........2.....93.........81.1..7...897...2.6...2.35..."
        for col in range(9):
            for row in range(9):
                command=("self.label"+str(row)+str(col)+".text = \"" + input[row*9+col] + "\"")
                exec(command)

class TestApp(App):
    def build(self):
        return Boxes()


if __name__ == '__main__':
    TestApp().run()