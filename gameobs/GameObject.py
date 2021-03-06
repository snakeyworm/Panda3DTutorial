
from direct.actor.Actor import Actor
from panda3d.core import Vec3
from panda3d.core import CollisionSphere, CollisionNode

FRICTION = 150.0

class GameObject():
    
    def __init__( self, pos, modelName, modelAnims, maxHealth, maxSpeed, colliderName ):

        self.actor = Actor( modelName, modelAnims )
        self.actor.reparentTo( render )
        self.actor.setPos( pos )

        self.maxHealth = maxHealth
        self.health = maxHealth

        self.maxSpeed = maxSpeed

        self.velocity = Vec3( 0, 0, 0 )
        self.acceleration = 300.0

        self.walking = False

        colliderNode = CollisionNode( colliderName )
        colliderNode.addSolid( CollisionSphere( 0, 0, 0, 0.3 ) )
        self.collider = self.actor.attachNewNode( colliderNode )

        self.collider.setPythonTag( "owner", self )

        self.deathSound = None

    def update( self, dt ):

        speed = self.velocity.length()

        if speed > self.maxSpeed:

            self.velocity.normalize()
            self.velocity *= self.maxSpeed
            
            speed = self.maxSpeed

        if not self.walking:

            frictionVal = FRICTION*dt

            if frictionVal > speed:
                self.velocity.set( 0, 0, 0 )
            else:
                frictionVec = -self.velocity
                frictionVec.normalize()
                frictionVec *= frictionVal

                self.velocity += frictionVec

        self.actor.setPos( self.actor.getPos() + self.velocity*dt )

    def alterHealth( self, dHealth ):
        
        previousHealth = self.health

        self.health += dHealth

        if self.health > self.maxHealth:
            self.health = self.maxHealth

        if previousHealth > 0 and self.health <= 0 and self.deathSound is not None:
            self.deathSound.play()

    def cleanup( self ):

        if self.collider is not None and not self.collider.isEmpty():
            self.collider.clearPythonTag( "owner" )
            base.cTrav.removeCollider( self.collider )
            base.pusher.removeCollider( self.collider )

        if self.actor is not None:
            self.actor.cleanup()
            self.actor.removeNode()
            self.actor = None

        self.collider = None


