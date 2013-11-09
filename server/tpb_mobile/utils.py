from tpb import CATEGORIES

def match_category(category_name):
    '''
    returns the category class that matches category_name
    '''
    if category_name == "ALL":
        to_return = CATEGORIES.ALL
    elif category_name == "AUDIO":
        to_return = CATEGORIES.AUDIO
    elif category_name == "VIDEO":
        to_return = CATEGORIES.VIDEO
    elif category_name == "APPLICATIONS":
        to_return = CATEGORIES.APPLICATIONS
    elif category_name == "GAMES":
        to_return = CATEGORIES.GAMES
    elif category_name == "OTHER":
        to_return = CATEGORIES.OTHER
    else:
        to_return = None
    return to_return