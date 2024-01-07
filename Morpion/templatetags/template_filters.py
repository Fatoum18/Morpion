from django.template.defaultfilters import register



@register.filter
def get_symbol_player_id(game,player_id):
    if game and game.symbol and str(player_id) in game.symbol :
            return game.symbol[str(player_id)]  
    return ""