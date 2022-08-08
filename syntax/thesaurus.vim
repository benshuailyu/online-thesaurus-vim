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

if exists("b:current_syntax")
    finish
endif
let b:current_syntax = "thesaurus"

syntax case match

syntax keyword definition DEFINITION
syntax keyword syntax PART OF SPEECH
syntax keyword synonym SYNONYMS
syntax keyword antonym ANTONYMS

hi link definition DiffAdd
hi link syntax DiffAdd
hi link synonym DiffAdd
hi link antonym DiffAdd
