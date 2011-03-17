%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% CLAIO08 class for LaTeX files                 v1.1 Mar-23-2007 %%
%%                                                                %%
%% The regular article class commands still exist and may be used.%%
%% 10pt, 11pt and twocolumn options are disabled.                 %%
%%                                                                %%
%% \maketitle make the first page automatically                   %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{CLAIO08paper}[2007/09/11-14 CLAIO08 paper class]

\DeclareOption{10pt}{\OptionNotUsed}
\DeclareOption{11pt}{\OptionNotUsed}
\DeclareOption{twocolumn}{\OptionNotUsed}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}

\ProcessOptions\relax

\LoadClass[11pt,epsf,epsfig]{article}
\RequirePackage{calc}
\RequirePackage{indentfirst}

%% Title
\renewcommand{\maketitle}{%
 \newpage
 \thispagestyle{plain}
 \begin{minipage}[t][1cm][t]{16.3cm}
  \begin{flushright}
   \scriptsize
\vspace{-132pt}
  INVESTIGACION OPERATIVA 2010 - TRABAJO PRACTICO METAHEURISTICAS
  \end{flushright}
 \end{minipage}
 \begin{center}%
  \vspace{-108pt}%
  {%3
   \fontsize{14}{16}\selectfont
   \bfseries
    \MakeUppercase{\@title}
   \par
  }%3
  %\vspace{18pt}%
 \vspace{13pt}%
  {%4
\fontsize{12}{14}\selectfont
   \bfseries\@author
   \par
  }%4
  %\vspace{14pt}%
  \vspace{10pt}%
  {%5
\fontsize{11}{12}\selectfont
   %\def\and{\\\vspace{14pt}}
\def\and{\\\vspace{13pt}}
   \normalfont\@address
   \par
  }%5
 \end{center}
 %\vspace{18pt}%
 %\vspace{5pt}%
 %\noindent\textbf{Key words:\space}\@keywords
 %\par
 %\vspace{18pt}%
 %\vspace{12pt}%
 %\noindent\textbf{Abstract.\space}{\textit\@abstract}
 %\par
%\vspace{18pt}%
 %\vfill
 %\newpage
}% End of \@maketitle

\def\author{\@ifnextchar[{\@getshortauthor}{\@getauthor}}
\def\@getauthor#1{\gdef\@author{#1}\gdef\@shortauthor{#1}}
\def\@getshortauthor[#1]#2{\gdef\@shortauthor{#1}\gdef\@author{#2}}

\newcommand{\address}[1]{\gdef\@address{#1}}

\newcommand{\keywords}[1]{\gdef\@keywords{#1}}

\renewcommand{\abstract}[1]{\gdef\@abstract{#1}}

\newcommand{\heading}[1]{\gdef\@heading{#1}}

\def\ps@myheadings{%
    \def\@oddfoot{\normalfont\hfil\thepage\hfil}
    \let\@evenfoot\@oddfoot
    \def\@evenhead{%
        %\parbox[t][11.5pt][t]{\textwidth}{%
\parbox[t][12,5pt][t]{\textwidth}{%
        \centering
        \normalfont
        \fontsize{10}{10}\selectfont
        \@heading\\
\vspace{-.2cm}
        \rule{\textwidth}{1pt}%
     }
    }%
    \let\@oddhead\@evenhead
    \let\@mkboth\@gobbletwo
    \let\sectionmark\@gobble
    \let\subsectionmark\@gobble
}

\def\sectionLevel{1}
\def\sectionIndent{0pt}
\def\sectionSpaceBefore{12pt}
\def\sectionSpaceAfter{6pt}
\def\sectionStyle{\normalsize\bfseries\MakeUppercase}

\renewcommand{\section}{%
  \@startsection{section}{\sectionLevel}{\sectionIndent}{\sectionSpaceBefore}%
                {\sectionSpaceAfter}{\sectionStyle}}%


\def\sectionLevel{2}
\def\sectionIndent{0pt}
\def\sectionSpaceBefore{12pt}
\def\sectionSpaceAfter{6pt}
\def\sectionStyle{\normalsize\bfseries}

\renewcommand{\subsection}{%
  \@startsection{subsection}{\sectionLevel}{\sectionIndent}{\sectionSpaceBefore}%
                {\sectionSpaceAfter}{\sectionStyle}}%


\renewcommand{\@makecaption}[2]{%
  \vskip\abovecaptionskip
  \sbox\@tempboxa{\normalsize\fontsize{10}{12}\selectfont #1: #2}%
  \ifdim \wd\@tempboxa >\hsize
    \normalsize\fontsize{10}{12}\selectfont #1: #2\par
  \else
    \global \@minipagefalse
    \hb@xt@\hsize{\hfil\box\@tempboxa\hfil}%
  \fi
  \vskip\belowcaptionskip}

\renewenvironment{thebibliography}[1]
  {%\newpage
   \section*{\MakeUppercase\refname\@mkboth{\MakeUppercase\refname}{\MakeUppercase\refname}}%
   \list{\@biblabel{\@arabic\c@enumiv}}%
        {\settowidth\labelwidth{\@biblabel{#1}}%
         \leftmargin\labelwidth
         \advance\leftmargin\labelsep
         \@openbib@code
         \usecounter{enumiv}%
         \let\p@enumiv\@empty
         \renewcommand\theenumiv{\@arabic\c@enumiv}}%
   \sloppy
   \clubpenalty4000
   \@clubpenalty \clubpenalty
   \widowpenalty4000%
   \sfcode`\.\@m}
  {\def\@noitemerr
   {\@latex@warning{Empty `thebibliography' environment}}%
   \endlist}
\setlength{\oddsidemargin}{0mm}
\setlength{\textheight}{220mm}
\setlength{\textwidth}{163mm}
\setlength{\textfloatsep}{12pt}
\setlength{\abovedisplayskip}{2pt}
\setlength{\belowdisplayskip}{6pt}
\setlength{\parindent}{0mm}
\setlength{\abovecaptionskip}{6pt}
\setlength{\belowcaptionskip}{6pt}
\setlength{\itemsep}{0pt}

\AtBeginDocument{%
  \pagestyle{empty}
  \maketitle
  \let\maketitle\relax
}

\endinput
