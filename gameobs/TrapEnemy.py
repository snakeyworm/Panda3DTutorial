
from gameobs.Enemy import *
from panda3d.core import BitMask32
import math

class TrapEnemy( Enemy ):

    def __init__( self, pos ):
        Enemy.__init__( self, pos,
            "models/SlidingTrap/trap", {
                "stand": "models/SlidingTrap/trap-stand",
                "walk": "models/SlidingTrap/trap-walk",
            },
            100.0,
            10.0,
            "trapEnemy" )

        base.pusher.addCollider( self.collider, self.actor )
        base.cTrav.addCollider( self.collider, base.pusher )

        self.moveInX = False

        self.moveDirection = -1.0

        self.ignorePlayer = False

        mask = BitMask32()

        mask.setBit( 2 )
        mask.setBit( 1 )

        self.collider.node().setIntoCollideMask( mask )

        mask = BitMask32()

        mask.setBit( 2 )
        mask.setBit( 1 )

        self.collider.node().setFromCollideMask( mask )

        self.impactSound = loader.loadSfx( "sounds/trapHitsSomething.ogg" )
        self.stopSound = loader.loadSfx( "sounds/trapStop.ogg" )
        self.movementSound = loader.loadSfx( "sounds/trapSlide.ogg" )

        self.movementSound.setLoop( True )

    def runLogic( self, player, dt ):

        if self.moveDirection != 0:

            self.walking = True
            if self.moveInX:
                self.velocity.addX( self.moveDirection * self.acceleration*dt )
            else:
                self.velocity.addY( self.moveDirection * self.acceleration*dt )

        else:
            self.walking = False
            diff = player.actor.getPos() - self.actor.getPos()

            if self.moveInX:
                detector = diff.y
                movement = diff.x
            else:
                detector = diff.x
                movement = diff.y


            if abs( detector ) < 0.5:
                self.moveDirection = math.copysign( 1, movement )
                self.movementSound.play()

    def alterHealth( self, dHealth ):
        pass

    def cleanup( self ):
        self.movementSound.stop()

        Enemy.cleanup( self )
