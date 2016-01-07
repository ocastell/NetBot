#!/bin/bash
LANG=$1
TEXT=$2

echo $TEXT $LANG

echo $TEXT | espeak -v $LANG
