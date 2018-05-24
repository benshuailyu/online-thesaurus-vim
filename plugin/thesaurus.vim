" File: thesaurus.vim
" Author: Benshuai Lyu
" License: GPLv3
" Description: 
" 	" This is a vim script wrapper for the python plugin which
"	" retrieves the thesaurus of the given requested word from
" 	" the website at www.thesaurus.com. Original idea comes from
	"  Anton Beloglazov <http://beloglazov.info/> 
	"  and
	"  Nick Coleman <http://www.nickcoleman.org/>
	" This specific wraper file (2nd half) exposes a handful of
" 	" necessary commands and keymaps to users. Another wrapper
" 	" file (1st half) bridges the graps between python and  
" 	" vim script is under autload for efficiency considerations.


if exists("g:ONLINE_THESAURUS")
    finish
endif
let g:ONLINE_THESAURUS = 1


"create default mapping 
"
if !exists("g:use_default_key_map")

    let g:use_default_key_map = 1

endif

if (g:use_default_key_map)

    nnoremap <Leader>t :call thesaurusPy2Vim#Thesaurus_LookCurrentWord()<CR>
    command! ThesaurusCurrent :call thesaurusPy2Vim#Thesaurus_LookCurrentWord()
    command! -nargs=1 Thesaurus :call thesaurusPy2Vim#Thesaurus_LookWord(<q-args>)

endif
