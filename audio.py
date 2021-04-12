#!/usr/bin/python

import audiogen
import sys
from audiogen.util import constant

#audiogen.sampler.write_wav(sys.stdout, audiogen.tone(440))
audiogen.sampler.play(
        audiogen.util.mixer(
            (audiogen.tone(50),audiogen.tone(52)),
            [(constant(0.3), constant(0.3)),]
            )
        )

