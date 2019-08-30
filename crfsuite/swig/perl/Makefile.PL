use 5.008;
use strict;
use warnings;
use ExtUtils::MakeMaker;

WriteMakefile(
    'CC' => 'g++',
    'LD' => 'g++',
    'NAME' => 'crfsuite',
    'VERSION' => '0.12',
    'OBJECT' => 'crfsuite.o export_wrap.o',
    'OPTIMIZE' => '-O2',
    'INC' => '-I../../include',
    );

