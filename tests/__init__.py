    # for letter in text:
    #     try:
    #         entries = _os_keyboard.map_name(normalize_name(letter))
    #         scan_code, modifiers = next(iter(entries))
    #     except (KeyError, ValueError) as err:
    #         _os_keyboard.type_unicode(letter)
    #         _time.sleep(0.2)
    #         continue
            
    #     for modifier in modifiers:
    #         press(modifier)

    #     _os_keyboard.press(scan_code)
    #     _os_keyboard.release(scan_code)

    #     for modifier in modifiers:
    #         release(modifier)

    #     _time.sleep(0.2)