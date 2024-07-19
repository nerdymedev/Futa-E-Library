from werkzeug.security import check_password_hash

def access_pass(password, hashed_password):
    return check_password_hash(hashed_password, password)

# Example usage
hashed_password = 'scrypt:32768:8:1$nSM23vpTQx1utPjJ$77a157ce6251bbaf6978ee57d9b559e6f0da7e6e0d0220a84d94ade0234fe29fb54422e557da853eb91160d06e52a0cadd07558aab20fa0d6ce23a8a7858fe73'
plaintext_password = 'Victoria'

result = access_pass(plaintext_password, hashed_password)
print(result)  
