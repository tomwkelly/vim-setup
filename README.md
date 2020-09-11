# Vim Commands
[Surround](#surround)

[Comment](#comment)

[Navigation](#navigation)

[Replacing](#replacing)

[Search and replace](#search-and-replace)

## Surround

### s
Main key, used in conjunction

### ysiw
Surround inner word

*ysiw' - surround word with '*

### `V<number><movement>S`
Wrap multiple lines in tag - useful for wrapping other tags

*`V5jS<div> - surround next 5 lines with <div>`*

### cs
Change surrounding

*`cs'<p> - change surrounding ' to <p>`*

*`cst<p> - change surrounding tag to <p>`*

*`cst<p - change surrounding tag to <p` __keeps attributes__*

### ds
Delete surrounding
*ds' - delete surrounding '*

## Comment

### cml
Comment line `(can also use cmd+/)`

### cmj
Comment line and line down

## Navigation

### gg
Move to top of file

### G
Move to end of file

### mx
Set mark x at current cursor position

### 'x
jump to beginning of line of mark x

### '' `(Two single quotes)`
Return to the line where the cursor was before the latest jump


### s
Sneak - finds the next occurence two characters typed

*eg. "sab" will find the next occurence of ab*

Can be used with ; and , to go to next and previous occurence respectively

### t
Go to character before searched

### f
Go to character searched

## Replacing

### r
Replace character `(returns to normal mode)`

### c
Replace, follow with what to replace 

*eg. c: line, w: word, t: tag ': single-quotes, etc.* 

## Search and replace

### :%s/foo/bar/g

Find each occurence of foo in all lines and replace with bar

### :<zero-width-space>s/foo/bar/g
Find each occurence of foo in current line and replace with bar
