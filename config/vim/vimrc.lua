" KEEP IN MIND THAT THIS ISN'T ACTUALLY written in Lua"
syntax on

" use spaces instead of tabs
set expandtab

" set 1 tab to 4 spaces
set shiftwidth=4
set tabstop=4

" show line number
set number
set numberwidth=2

" when opening a new file with split, open the file at the bottom or right panel
set splitbelow
set splitright

"highlight searches in vim
set hlsearch

" press esc to remove highlight, # NOTE: while this works, remapping ESC
" results in strange behavior
" map <esc> :noh <CR>

" instead remmap to the "return"/"space" key, it must be pressed twice in
" command mode
nnoremap <CR> :noh<CR><CR>

" set this if using vim inside tmux
set background=dark

" add command to save file with priviliges
command W :execute ':silent w !sudo tee % > /dev/null' | :edit!


" #FIXME: install vim plugins somehow"
"""""""""""""""""""""""""""set up plugins here""""""""""""""""""""""""""""
" once done, reload file with :source % and then install with :PlugInstall

" call plug#begin()

" Surround vim plugin: https://vimawesome.com/plugin/surround-vim
" Plug 'tpope/vim-surround'

" Vim Multiple Cursors: https://vimawesome.com/plugin/vim-multiple-cursors
" Plug 'terryma/vim-multiple-cursors'

" You Complete Me plugin:  https://vimawesome.com/plugin/youcompleteme FYI, this has more involved installation process (it needs to be compiled)
" FYI this has a more involved installation process, it needs to be compiled
" Plug 'valloric/youcompleteme', { 'do': './install.py' }

" Vim Polygot: https://vimawesome.com/plugin/vim-polyglot
" set up polygot plugin
" let mapleader = "\<Space>"
" set nocompatible
" Plug 'sheerun/vim-polyglot'

" Markdown Syntax: https://vimawesome.com/plugin/markdown-syntax
" set up vim markdown plugin
" Plug 'plasticboy/vim-markdown'

" let g:markdown_fenced_languages = ['html', 'py=python', 'ruby']
" let g:vim_markdown_auto_extension_ext = 'txt'
" let g:vim_markdown_folding_disabled = 1
" let g:vim_markdown_math = 1
" let g:vim_markdown_frontmatter = 1
" let g:vim_markdown_toml_frontmatter = 1
" let g:vim_markdown_json_frontmatter = 1

" call plug#end()
