# sudo mv pifacecadshutdown /etc/init.d/
# sudo update-rc.d pifacecadshutdown stop 99 0 .

import pifacecad as p

cad = p.PiFaceCAD()
cad.lcd.backlight_on()
cad.lcd.cursor_off()
cad.lcd.blink_off()

cad.lcd.set_cursor(6,0)
cad.lcd.write("Shutdown")
cad.lcd.set_cursor(6,1)
cad.lcd.write("Complete")

# K over 4 chars (down, left)
cg = p.LCDBitmap([24,24,24,25,27,31,30,28])
cad.lcd.store_custom_bitmap(0, cg)
cg = p.LCDBitmap([28,30,31,27,25,24,24,24])
cad.lcd.store_custom_bitmap(1, cg)
cg = p.LCDBitmap([6,14,28,24,16,0,0,0])
cad.lcd.store_custom_bitmap(2, cg)
cg = p.LCDBitmap([0,0,0,16,24,28,14,6])
cad.lcd.store_custom_bitmap(3, cg)

# V over 4 chars (down, left)
cg = p.LCDBitmap([24,24,24,12,12,12,6,6])
cad.lcd.store_custom_bitmap(4, cg)
cg = p.LCDBitmap([6,6,3,3,3,1,1,1])
cad.lcd.store_custom_bitmap(5, cg)
cg = p.LCDBitmap([3,3,3,6,6,6,12,12])
cad.lcd.store_custom_bitmap(6, cg)
cg = p.LCDBitmap([12,12,24,24,24,16,16,16])
cad.lcd.store_custom_bitmap(7, cg)

cad.lcd.set_cursor(1,0)
cad.lcd.write_custom_bitmap(0)
cad.lcd.write_custom_bitmap(2)
cad.lcd.write_custom_bitmap(4)
cad.lcd.write_custom_bitmap(6)
cad.lcd.set_cursor(1,1)
cad.lcd.write_custom_bitmap(1)
cad.lcd.write_custom_bitmap(3)
cad.lcd.write_custom_bitmap(5)
cad.lcd.write_custom_bitmap(7)