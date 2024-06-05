text = "01234567890"
split_text = []
for i in range(0, len(text), 2):
    if i < len(text) - 1:
        split_text.append(text[i:i + 2])
    else:
        split_text.append(text[i:] + "_")
print(split_text)
# Output: ['01', '23', '45', '67', '89', '0_']