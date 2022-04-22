
from gameobs.Enemy import *
from panda3d.core import Vec2

class WalkingEnemy( Enemy ):

    def __init__( self, pos ):

        Enemy.__init__( self, pos, "models/SimpleEnemy/simpleEnemy", {
                        "stand": "models/SimpleEnemy/simpleEnemy-stand",
                        "walk": "models/SimpleEnemy/simpleEnemy-walk",
                        "attack": "models/SimpleEnemy/simpleEnemy-attack",
                        "die": "models/SimpleEnemy/simpleEnemy-die",
                        "spawn": "models/SimpleEnemy/simpleEnemy-spawn",
                    },
                    3.0,
                    7.0,
                    "walkingEnemy"
        )

        self.attackDistance = 0.75
        self.acceleration = 100.0

        self.yVector = Vec2( 0, 1 )

    def runLogic( self, player, dt ):

        vectorToPlayer = player.actor.getPos() - self.actor.getPos()

        vectorToPlayer2D = vectorToPlayer.getXy()
        distanceToPlayer = vectorToPlayer2D.length()

        vectorToPlayer2D.normalize()

        if distanceToPlayer > self.attackDistance*0.9:
            self.walking = True

            vectorToPlayer.setZ( 0 )
            vectorToPlayer.normalize()
            self.velocity += vectorToPlayer*self.acceleration*dt

        else:

            self.walking = False
            self.velocity.set( 0, 0, 0 )

        heading = self.yVector.signedAngleDeg( vectorToPlayer2D )
        self.actor.setH( heading )
    

