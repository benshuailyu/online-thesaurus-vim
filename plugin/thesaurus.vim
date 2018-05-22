" File: thesaurus.vim
" Author: Benshuai Lyu
" License: GPLv3
" Description: 
" 	" This is a vim script wrapper for the python plugin, which
"	" retrieves the thesaurus of the given requested word from
" 	" the website at www.thesaurus.com. Original idea comes from
	"  Anton Beloglazov <http://beloglazov.info/> 
	"  and
	"  Nick Coleman <http://www.nickcoleman.org/>


if exists("g:ONLINE_THESAURUS")
    finish
endif
let g:ONLINE_THESAURUS = 1



"take the import outside so that you don't need to import 
"evertime you call the function

python import vim
python import sys
"
"append sys.path so that modules can be found
"relative path import only works with  package
let s:currentScriptPath = expand('<sfile>:p:h')
let s:modulePath = s:currentScriptPath . '/../modules/'
python sys.path.append(vim.eval('s:modulePath'))
python from extract_thesaurus import *

" note you cannot use python 'from extract_thesaurus import *' 
" because these "quotes will be carried over and the python
" statement is a string obj.

function! Thesaurus_LookWord(word)

    exec ":silent belowright 10split thesaurus-for-" . a:word

    setlocal noswapfile nobuflisted nospell modifiable
    setlocal buftype=nofile bufhidden=hide
    nnoremap <silent> <buffer> q :q<CR>

    "noting the following way of argument passing through vim module
    "Note you cannot indent the closing EOF

python << EOF
definition_family_list = online_thesaurus(vim.eval("a:word"))

cb = vim.current.buffer
cb[:]=None # delete everything in the buffer just in case

for each_family in definition_family_list:
    cb.append("DEFINITION: " + each_family._definition)
    cb.append("PART OF SPEECH: " + each_family._syntax)
    cb.append('SYNONYMS: '  +
              ', '.join(each_family._synonyms))
    cb.append('ANTONYMS: ' +
              ', '.join(each_family._antonyms))
    cb.append(' ')
# note the buffer appending starts from the second line.
# delete the first empt
cb[0] = None
EOF
setlocal nomodifiable filetype=thesaurus
endfunction


function! Thesaurus_LookCurrentWord()

    let currentWord = expand("<cword>")
    call Thesaurus_LookWord(currentWord)

endfunction



"create default mapping 
"
if !exists("g:use_default_key_map")

    let g:use_default_key_map = 1

endif

if (g:use_default_key_map)

    nnoremap <Leader>t :call Thesaurus_LookCurrentWord()<CR>
    command! ThesaurusCurrent :call Thesaurus_LookCurrentWord()
    command! -nargs=1 Thesaurus :call Thesaurus_LookWord(<q-args>)

endif
