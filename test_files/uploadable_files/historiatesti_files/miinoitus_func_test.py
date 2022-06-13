import importlib
import random
import test_core as core

st_function = {
    "fi": "miinoita",
    "en": "place_mines"
}

st_draw_function = {
    "fi": "piirra_kentta",
    "en": "draw_field"
}

st_main_function = {
    "fi": "main",
    "en": "main"
}

sweeperlib = {
    "fi": "haravasto",
    "en": "sweeperlib"
}


field_key = {
    "fi": "kentta",
    "en": "field"
}

funcdict = core.TranslationDict()
funcdict.set_msg("clear_window", "fi", "tyhjaa_ikkuna")
funcdict.set_msg("clear_window", "en", "clear_window")
funcdict.set_msg("start_tile_buffer", "fi", "aloita_ruutujen_piirto")
funcdict.set_msg("start_tile_buffer", "en", "begin_sprite_draw")
funcdict.set_msg("buffer_add_tile", "fi", "lisaa_piirrettava_ruutu")
funcdict.set_msg("buffer_add_tile", "en", "prepare_sprite")
funcdict.set_msg("draw_tile_buffer", "fi", "piirra_ruudut")
funcdict.set_msg("draw_tile_buffer", "en", "draw_sprites")
funcdict.set_msg("draw_background", "fi", "piirra_tausta")
funcdict.set_msg("draw_background", "en", "draw_background")
funcdict.set_msg("start", "fi", "aloita")
funcdict.set_msg("start", "en", "start")


rnd_msgs = core.TranslationDict()
rnd_msgs.set_msg("CorrectResult", "fi", "Funktio asetti oikean määrän miinoja satunnaisesti.")
rnd_msgs.set_msg("CorrectResult", "en", "The function placed the correct amount of mines randomly.")
rnd_msgs.set_msg("PrintStudentResult", "fi", "Funktio asetti {res} miinaa.")
rnd_msgs.set_msg("PrintStudentResult", "en", "The function placed {res} mines.")
rnd_msgs.set_msg("PrintReference", "fi", "Olisi pitänyt asettaa {ref} miinaa.")
rnd_msgs.set_msg("PrintReference", "en", "Should have placed {ref} mines.")
rnd_msgs.set_msg("fail_mine_count", "fi", dict(
    content="Funktio asetti väärän määrän miinoja.",
    hints=["Varmista, että miinoitusfunktio ei yritä miinoittaa samaa ruutua kahdesti."],
    triggers=["miinoitus-koordinaattiparit"]
))
rnd_msgs.set_msg("fail_mine_count", "en", dict(
    content="The function placed the wrong amount of mines.",
    hints=["Make sure your function doesn't attempt to mine the same tile twice."],    
    triggers=["miinoitus-koordinaattiparit"]
))
rnd_msgs.set_msg("fail_randomness", "fi", dict(
    content="Funktio antoi kahdesti peräkkäin saman miinoituksen.",
    hints=["Varmista, että miinoitusfunktio käyttää satunnaisuutta.", "Kokeile palauttaa koodi uudestaan - todennäköisyys samaan satunnaistulokseen kahdesti peräkkäin on aina olemassa."],
))
rnd_msgs.set_msg("fail_randomness", "en", dict(
    content="The function exactly the same mine mine placement twice.",
    hints=["Make sure the mining function uses proper randomness.", "You try to return the code again - the odds of getting the same placement twice are miniscule, but existing."],
))

draw_msgs = core.TranslationDict()
draw_msgs.set_msg("CorretResult", "fi", "Piirtokäsittelijä toimi oikein.")
draw_msgs.set_msg("CorretResult", "en", "The draw handler functioned correctly.")
draw_msgs.set_msg("PrintStudentResult", "fi", "Funktio piirsi alla listatuilla funktioilla {res[3]}x{res[4]} kentän, jossa ruutujen koko oli {res[2]}, ja kentällä yhteensä {res[1]} miinaa:\n{res[0]}")
draw_msgs.set_msg("PrintStudentResult", "en", "The function used the functions listed below to draw a {res[3]}x{res[4]} field with a tile size of {res[2]}, with a total of {res[1]} mines:\n{res[0]}")
draw_msgs.set_msg("PrintReference", "fi", "Olisi pitänyt käyttää alla listattuja funktioita ja piirtää {ref[3]}x{ref[4]} kenttä, jossa ruutujen koko on {ref[2]}, ja kentällä yhteensä {ref[1]} miinaa:\n{ref[0]}")
draw_msgs.set_msg("PrintReference", "en", "Should have used the functions listed below to draw a {ref[3]}x{ref[4]} field with a tile size of {ref[2]}, with a total of {ref[1]} mines:\n{ref[0]}")
draw_msgs.set_msg("fail_inject", "fi", dict(
    content="Tarkistuskentän asettaminen ohjelman tilasanakirjaan epäonnistui.",
    hints=["Tehtävässä tulee käyttää ohjeiden mukaista tilasanakirjaa."],
    triggers=["miinoitus-tilasanakirja"]
))
draw_msgs.set_msg("fail_inject", "en", dict(
    content="Setting the test field to the program's state dictionary failed.",
    hints=["You must use a state dictionary as told in the instructions."],
    triggers=["miinoitus-tilasanakirja"]
))
draw_msgs.set_msg("fail_no_clear", "fi", dict(
    content="Ikkunaa ei tyhjenetty piirtämisen alussa.",
    hints=["Lue haravaston piirtokäsittelijäohjeet aseta_piirto_kasittelija-funktion dokumentaatiomerkkijonosta.", "Tarkista, että ikkuna tyhjätään piirtämisen alussa."],
))
draw_msgs.set_msg("fail_no_clear", "en", dict(
    content="The window was not cleared before drawing.",
    hints=["Read how to make a draw handler from the register_draw_handler function docstring.", "Make sure the window is cleared first."],
))
draw_msgs.set_msg("fail_no_start_buffer", "fi", dict(
    content="Piirtokäsittelijä ei alustanut piirtopuskuria.",
    hints=["Lue haravaston piirtokäsittelijäohjeet aseta_piirto_kasittelija-funktion dokumentaatiomerkkijonosta.", "Piirtopuskuri tulee alustaa ennen kuin siihen voidaan lisätä piirrettäviä ruutuja."],
))
draw_msgs.set_msg("fail_no_start_buffer", "en", dict(
    content="The draw handler didn't initialize the tile buffer.",
    hints=["Read how to make a draw handler from the register_draw_handler function docstring.", "The tile buffer must be initialized before adding tiles to it."],
))
draw_msgs.set_msg("fail_no_draw", "fi", dict(
    content="Piirtopuskurin sisältöä ei piirretty ruudulle.",
    hints=["Lue haravaston piirtokäsittelijäohjeet aseta_piirto_kasittelija-funktion dokumentaatiomerkkijonosta.", "Jotta ruudulle tulisi jotain näkyviin, tulee piirtämisen päätteeksi kutsua piirra_ruudut-funktiota."],
))
draw_msgs.set_msg("fail_no_draw", "en", dict(
    content="The contents of the tile buffer were not drawn.",
    hints=["Read how to make a draw handler from the register_draw_handler function docstring.", "In order to actually draw tiles on the screen, you need to call the draw_tile_buffer function."],
))
draw_msgs.set_msg("fail_clear_not_first", "fi", dict(
    content="Ikkunan tyhjennystä ei tehty piirtokäsittelijässä ensimmäisenä.",
    hints=["Lue haravaston piirtokäsittelijäohjeet aseta_piirto_kasittelija-funktion dokumentaatiomerkkijonosta."],
))
draw_msgs.set_msg("fail_clear_not_first", "en", dict(
    content="Clearing the window was not done first.",
    hints=["Read how to make a draw handler from the register_draw_handler function docstring."],
))
draw_msgs.set_msg("fail_start_buffer_not_second", "fi", dict(
    content="Piirtopuskurin alustusta ei tehty ennen piirrettävien ruutujen lisäämistä.",
    hints=["Lue haravaston piirtokäsittelijäohjeet aseta_piirto_kasittelija-funktion dokumentaatiomerkkijonosta."],
))
draw_msgs.set_msg("fail_start_buffer_not_second", "en", dict(
    content="Initializing the tile buffer was not done before adding tiles.",
    hints=["Read how to make a draw handler from the register_draw_handler function docstring."],
))
draw_msgs.set_msg("fail_draw_not_last", "fi", dict(
    content="Piirtopuskurin sisällön piirtäminen ei ollut viimeinen kutsuttu funktio.",
    hints=["Lue haravaston piirtokäsittelijäohjeet aseta_piirto_kasittelija-funktion dokumentaatiomerkkijonosta."],
))
draw_msgs.set_msg("fail_draw_not_last", "en", dict(
    content="Drawing the tile buffer was not done last.",
    hints=["Read how to make a draw handler from the register_draw_handler function docstring."],
))
draw_msgs.set_msg("fail_coordinates", "fi", dict(
    content="Piirtokäsittelijä piirsi ruutuja vääriin ruutukoordinaatteihin.",
    hints=["Tarkista, että ruutujen piirtoväli on sama kuin ruutujen koko.", "Ruutujen koon voit selvittää tutkimalla haravastoon kuuluvia grafiikkatiedostoja.", "Tarkista, että piirtäessä otat y-koordinaatin rivin indeksistä ja x-koordinaatin ruudun indeksistä rivin sisällä."],
))
draw_msgs.set_msg("fail_coordinates", "en", dict(
    content="The handler drew tiles in the wrong coordinates.",
    hints=["Make sure that tile spacing is the same as their size.", "You can find out the tile size by looking at the graphics files.", "Make sure you calculate the y coordinate from the row index and x coordinate from the column index."],
))
draw_msgs.set_msg("fail_mine_tile_count", "fi", dict(
    content="Piirtokäsittelijä ei piirtänyt oikeaa määrää miinoja.",
))
draw_msgs.set_msg("fail_mine_tile_count", "en", dict(
    content="The draw handler didn't draw the correct number of mines.",
))

static_msgs = core.TranslationDict()
static_msgs.set_msg("fail_no_start", "fi", dict(
    content="Pääohjelmafunktiosta puuttuu haravasto.aloita-funktiokutsu, joten ohjelman ei lähde käyntiin.",
    hints=["Muista lisätä haravasto.aloita() main-funktioon."]
))
static_msgs.set_msg("fail_no_start", "en", dict(
    content="The main function is missing a call to sweeperlib.start. The program will not actually run.",
    hints=["Remember to call sweeperlib.start in the main function."]
))

calls = []
prev = []
drawn_field = {}
symbols = "0123456789xf "
tiles = dict(zip(symbols, symbols))

def gen_vector():
    v = []
    
    for i in range(5):
        rw = random.randint(16, 20)
        rh = random.randint(11, 15)
        pairs = []
        pairs_copy = []
        for x in range(rw):
            for y in range(rh):
                pairs.append((x, y))
                pairs_copy.append((x, y))

        room = []
        room_copy = []
        for row in range(rh):
            room.append([])
            room_copy.append([])
            for col in range(rw):
                room[-1].append(" ")                
                room_copy[-1].append(" ")
                
        n = random.randint(1, rw * rh // 2)
        
        v.append((room, pairs, n))
        v.append((room_copy, pairs_copy, n))

    return v

def ref_random_func(field, pairs, n):
    return n

def field_extractor(args, res, parsed):
    return args[0]

def count_mines(room):
    n = 0
    for row in room:
        for col in row:
            if col == "x":
                n += 1
    return n

def count_diff(room, prev):
    diff = 0
    for r in range(len(room)):
        for c in range(len(room[0])):
            if room[r][c] != prev[r][c]:
                diff += 1
    return diff

def copy_room(args):
    new = []
    for r in args[0]:
        new.append([])
        for c in r:
            new[-1].append(c)
    return new, args[1][:], args[2] 

def random_validator(ref, res, parsed):
    global prev
    temp = prev
    prev = res
    assert count_mines(res) == ref, "fail_mine_count"
    if len(res) == len(temp) and len(res[0]) == len(temp[0]):
        assert count_diff, "fail_randomness"
    

def ref_draw_func():
    n = len(prev) * len(prev[0])
    ref_calls = [
        funcdict.get_msg("clear_window", lang), 
        funcdict.get_msg("start_tile_buffer", lang),
    ]
    for i in range(n):
        ref_calls.append(funcdict.get_msg("buffer_add_tile", lang))
        
    ref_calls.append(funcdict.get_msg("draw_tile_buffer", lang))
    
    ref_drawn = {}
    for r, row in enumerate(prev):
        for c, tile in enumerate(row):
            ref_drawn[(c * 40, r * 40)] = tile
            
    return ref_calls, ref_drawn
            

def draw_extractor(args, res, parsed):
    return calls, drawn_field

def draw_validator(ref, res, parsed):    
    assert inject_ok, "fail_inject"
    while funcdict.get_msg("draw_background", lang) in res[0]:
        res[0].remove(funcdict.get_msg("draw_background", lang))
        
    assert funcdict.get_msg("clear_window", lang) in res[0], "fail_no_clear"
    assert funcdict.get_msg("start_tile_buffer", lang) in res[0], "fail_no_start_buffer"
    assert funcdict.get_msg("draw_tile_buffer", lang) in res[0], "fail_no_draw"
    assert res[0][0] == funcdict.get_msg("clear_window", lang), "fail_clear_not_first"
    assert res[0][1] == funcdict.get_msg("start_tile_buffer", lang), "fail_start_buffer_not_second"
    assert res[0][-1] == funcdict.get_msg("draw_tile_buffer", lang), "fail_draw_not_last"
    assert res[0].count(funcdict.get_msg("buffer_add_tile", lang)) == ref[0].count(funcdict.get_msg("buffer_add_tile", lang)), "fail_add_tile_count"
    
    pairs = list(res[1].keys())
    pairs.sort()
    x_offset = pairs[0][0]
    y_offset = pairs[0][1]
    if x_offset or y_offset:
        pairs = [(x - x_offset, y - y_offset) for x, y in pairs]
    ref_pairs = list(ref[1].keys())
    ref_pairs.sort()
    
    assert tuple(pairs) == tuple(ref_pairs), "fail_coordinates"    
    assert list(res[1].values()).count("x") == list(ref[1].values()).count("x"), "fail_mine_tile_count"
    
inject_ok = False

def inject_field(args, inputs):
    global inject_ok
    for name in dir(st_module):
        if isinstance(getattr(st_module, name), dict):
            if name not in dir(lib_mod):
                if field_key[lang] in getattr(st_module, name):
                    getattr(st_module, name)[field_key[lang]] = prev
                    inject_ok = True
                    return

def dummy_clear():
    calls.append(funcdict.get_msg("clear_window", lang))

def dummy_start_buffer():
    calls.append(funcdict.get_msg("start_tile_buffer", lang))

def dummy_add_tile(key, x, y):
    calls.append(funcdict.get_msg("buffer_add_tile", lang))    
    drawn_field[(x, y)] = tiles[key]

def dummy_draw():
    calls.append(funcdict.get_msg("draw_tile_buffer", lang))

def draw_output_presenter(value):
        call_list = value[0]
        field = value[1]
        n_drawn_tiles = call_list.count(funcdict.get_msg("buffer_add_tile", lang))
        while call_list.count(funcdict.get_msg("buffer_add_tile", lang)) > 1:
            call_list.remove(funcdict.get_msg("buffer_add_tile", lang))
        try:
            call_list[call_list.index(funcdict.get_msg("buffer_add_tile", lang))] += ", ... (x{})".format(n_drawn_tiles)        
        except:
            pass
        
        pairs = list(field.keys())
        pairs.sort()
        try:
            size_y = pairs[1][1] - pairs[0][1]
            pairs.sort(key=lambda x: x[1])
            size_x = pairs[1][0] - pairs[0][0]
            w = int((pairs[-1][0] + size_x) / size_x)
            h = int((pairs[-1][1] + size_y) / size_y)
        except:
            size_y = size_x = "?"    
            w = "?"
            h = "?"
            
        n_mine_tiles = list(field.values()).count("x")
        return "{{{highlight=python3\n" + str(call_list) + "\n}}}", n_mine_tiles, "{}x{}".format(size_x, size_y), w, h

def rnd_call_presenter(fn, value):
    callstr = fn + "(\n"
    fieldstr = str([str(row[:2]).rstrip("]") + ", ... ]" for row in value[0]][:3]).rstrip("]") + ", ... ]"
    callstr += "  " + fieldstr.replace("\"", "") + ", # ({}x{})\n".format(len(value[0][0]), len(value[0]))
    callstr += "  " + str(value[1][:3]).rstrip("]") + ", ... ], # ({})\n".format(len(value[1]))
    callstr += "  {}\n".format(value[2])
    callstr += ")"
    return "{{{highlight=python3\n" + callstr + "\n}}}"
        
    
def has_start(source, docs, comments):
    assert (funcdict.get_msg("start", lang) + "(") in source, "fail_no_start"
    

rnd_presenters = {
    "res": count_mines,
    "call": rnd_call_presenter
}

draw_presenters = {
    "res": draw_output_presenter,
    "ref": draw_output_presenter
}

if __name__ == "__main__":
    files, lang = core.parse_command()
    st_mname = files[0]   
    st_module = core.load_module(st_mname, lang, inputs=[])    
    if st_module:
        lib_mod = importlib.import_module(sweeperlib[lang])
        setattr(lib_mod, funcdict.get_msg("clear_window", lang), dummy_clear)
        setattr(lib_mod, funcdict.get_msg("start_tile_buffer", lang), dummy_start_buffer)
        setattr(lib_mod, funcdict.get_msg("buffer_add_tile", lang), dummy_add_tile)
        setattr(lib_mod, funcdict.get_msg("draw_tile_buffer", lang), dummy_draw)
        core.test_function(st_module, st_function, gen_vector, ref_random_func, lang, custom_msgs=rnd_msgs, validator=random_validator, presenter=rnd_presenters, result_object_extractor=field_extractor, argument_cloner=copy_room)
        if prev:
            core.test_function(st_module, st_draw_function, [[]], ref_draw_func, lang, custom_msgs=draw_msgs, validator=draw_validator, presenter=draw_presenters, result_object_extractor=draw_extractor, new_test=inject_field)                   
        core.static_test(st_module, st_main_function, lang, [has_start], custom_msgs=static_msgs)
        core.pylint_test(st_module, lang, extra_options=["--disable=unused-argument"])
    