#!/bin/bash

# Ejecutar desde el directorio del proyecto, es decir, un nivel antes de src
# Prerequisitos:
#   $ cd ~/Proyectos/Presentaciones/202304-Django-meetup
#   $ mkdir -p test_src/templates/customers
#   $ cp -i src/customers/templates/customers/*.html test_src/templates/customers/.

while IFS= read -r filename; do
    echo "$filename"
    awk '
    BEGIN{print "{% extends \"base.html\" %}\n\n{% block title %}{% endblock %}\n\n{% block content %}\n"}
    {print}
    END{print "\n{% endblock %}"}' "$filename" > "$filename".new && cp --preserve=all "$filename" "$filename".bak && mv "$filename".new  "$filename"
done < <( find test_src -path '*/templates/*' \( -name '*.html' ! -name 'base.html' \) -exec grep --files-without-match -i '{% extends "base.html" %}' {} \;)
