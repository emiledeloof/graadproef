from RPLCD.i2c import CharLCD # Bibliotheek importeren

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8) # Scherm initialiseren met juiste parameters 
lcd.clear() # scherm leegmaken indien er nog dingen op LCD staan

lcd.write_string('Tekst hier...') #Tekst op LCD zetten
