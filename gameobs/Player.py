
from gameobs.GameObject import *

class Player( GameObject ):
    
    def __init__( self ):
        GameObject.__init__(
                self,
                Vec3( 0, 0, 0 ), 
                "models/PandaChan/act_p3d_chan", {
                    "stand": "models/PandaChan/a_p3d_chan_idle",
                    "walk": "models/PandaChan/a_p3d_chan_run",
                },
                5,
                10,
                "player"
        )
        
        self.actor.getChild( 0 ).setH( 180 )

        base.pusher.addCollider( self.collider, self.actor )
        base.cTrav.addCollider( self.collider, base.pusher )

        self.actor.loop( "stand" )

    def update( self, keys, dt ):

        GameObject.update( self, dt )

        self.walking = False

        if keys[ "up" ]:
            self.walking = True
            self.velocity.addY( self.acceleration*dt )
        if keys[ "down" ]:
            self.walking = True
            self.velocity.addY( -self.acceleration*dt )
        if keys[ "left" ]:
            self.walking = True
            self.velocity.addX( -self.acceleration*dt ) 
        if keys[ "right" ]:
            self.walking = True
            self.velocity.addX( self.acceleration*dt ) 

        if self.walking:

            standControl = self.actor.getAnimControl( "stand" )
            if standControl.isPlaying():
                standControl.stop()

            walkControl = self.actor.getAnimControl( "walk" )
            if not walkControl.isPlaying():
                self.actor.loop( "walk" )

        else:

            standControl = self.actor.getAnimControl( "stand" )

            if not standControl.isPlaying():
                self.actor.stop( "walk" )
                self.actor.loop( "stand" )
