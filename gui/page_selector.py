HOME = 'Home'
SEND = 'Send'
RECEIVE = 'Receive'
KEY_VAULT = 'Key Vault'
PAGES = [HOME, SEND, RECEIVE, KEY_VAULT]

def page_selector(page_name: str):
    """
    Return the page class given the page name
    """
    if page_name == HOME:
        from home_page import HOME_PAGE
        return HOME_PAGE
    elif page_name == SEND:
        from send_page import SEND_PAGE
        return SEND_PAGE
    elif page_name == RECEIVE:
        from receive_page import RECEIVE_PAGE
        return RECEIVE_PAGE
    elif page_name == KEY_VAULT:
        from key_vault_page import KEY_VAULT_PAGE
        return KEY_VAULT_PAGE
    else:
        raise ValueError("Invalid page name")
        

