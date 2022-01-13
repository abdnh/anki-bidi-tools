.PHONY: all zip install clean

all: zip
zip: bidi_tools.ankiaddon

bidi_tools.ankiaddon: $(shell find src/ -type f)
	rm -f $@
	( cd src/; zip -r ../$@ * )

# install in test profile
install: zip
	unzip -o bidi_tools.ankiaddon -d ankiprofile/addons21/bidi_tools


clean:
	rm -f bidi_tools.ankiaddon
