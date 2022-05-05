from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import Vec4, Vec3
from panda3d.core import CollisionNode
from panda3d.core import CollisionTube
from panda3d.core import CollisionHandlerPusher
from panda3d.core import CollisionTraverser
from gameobs.Player import *
from gameobs.WalkingEnemy import *
from gameobs.TrapEnemy import *


class Game( ShowBase ):

    def __init__( self ):

        ShowBase.__init__( self )

        # Configure Window

        properties = WindowProperties()
        properties.setSize( 1000, 750 )
        self.win.requestProperties( properties )

        self.disableMouse()
        self.render.setShaderAuto()

        # Collision Handlers and Traversers

        self.pusher = CollisionHandlerPusher()
        self.cTrav = CollisionTraverser()

        self.pusher.setHorizontal( True )

        self.keyMap = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "shoot": False,
        }

        # Models

        self.environemnt = self.loader.loadModel(
            "models/Environment/environment" )
        self.environemnt.reparentTo( self.render )

        # Lights

        ambientLight = AmbientLight( "ambient light" )
        ambientLight.setColor( Vec4( 0.2, 0.2, 0.2, 1 ) )

        self.ambientLightNodePath = self.render.attachNewNode( ambientLight )
        self.render.setLight( self.ambientLightNodePath )

        mainLight = DirectionalLight( "main light" )
        self.mainLightNodePath = self.render.attachNewNode( mainLight )
        self.mainLightNodePath.setHpr( 45, -45, 0 )

        self.render.setLight( self.mainLightNodePath )

        # Actors

        self.player = Player()
        self.tempEnemy = WalkingEnemy( Vec3( 5, 0, 0 ) )
        self.tempTrap = TrapEnemy( Vec3( -2, 7, 0 ) )

        # Position camera
        self.camera.setPos( 0, 0, 32 )
        self.camera.setP( -90 )

        self.updateTask = taskMgr.add( self.update, "update" )

        # Events

        # Key Events

        self.accept( "w", self.updateKeyMap, [ "up", True ] )
        self.accept( "w-up", self.updateKeyMap, [ "up", False ] )
        self.accept( "s", self.updateKeyMap, [ "down", True ] )
        self.accept( "s-up", self.updateKeyMap, [ "down", False ] )
        self.accept( "a", self.updateKeyMap, [ "left", True ] )
        self.accept( "a-up", self.updateKeyMap, [ "left", False ] )
        self.accept( "d", self.updateKeyMap, [ "right", True ] )
        self.accept( "d-up", self.updateKeyMap, [ "right", False ] )
        self.accept( "mouse1", self.updateKeyMap, [ "shoot", True ] )
        self.accept( "mouse1-up", self.updateKeyMap, [ "shoot", False ] )

        self.pusher.add_in_pattern( "%fn-into-%in" )
        self.accept( "trapEnemy-into-wall", self.stopTrap )
        self.accept( "trapEnemy-into-trapEnemy", self.stopTrap )
        self.accept( "trapEnenmy-into-player", self.trapHitsSomething )
        self.accept( "trapEnemy-into-walkingEnemy", self.trapHitsSomething )


        wallSolid = CollisionTube( -8.0, 0, 0, 8.0, 0, 0, 0.2 )
        wallNode = CollisionNode( "wall" )
        wallNode.addSolid( wallSolid )
        wall = self.render.attachNewNode( wallNode )
        wall.setY( 8.0 )

        wallSolid = CollisionTube( -8.0, 0, 0, 8.0, 0, 0, 0.2 )
        wallNode = CollisionNode( "wall" )
        wallNode.addSolid( wallSolid )
        wall = self.render.attachNewNode( wallNode )
        wall.setY( -8.0 )

        wallSolid = CollisionTube( 0, -8.0, 0, 0, 8.0, 0, 0.2 )
        wallNode = CollisionNode( "wall" )
        wallNode.addSolid( wallSolid )
        wall = self.render.attachNewNode( wallNode )

        wall.setX( 8.0 )
        wallSolid = CollisionTube( 0, -8.0, 0, 0, 8.0, 0, 0.2 )
        wallNode = CollisionNode( "wall" )
        wallNode.addSolid( wallSolid )
        wall = self.render.attachNewNode( wallNode )
        wall.setX( -8.0 )

    def stopTrap( self, entry ):

        collider = entry.getFromNodePath()

        if collider.hasPythonTag( "owner" ):
            trap = collider.getPythonTag( "owner" )
            trap.moveDirection = 0
            trap.ignorePlayer = False
    
    def trapHitsSomething( self, entry ):
        collider = entry.getFromNodePath()

        if collider.hasPythonTag( "owner" ):
            trap = collider.getPythonTag( "owner" )

            if trap.moveDirection == 0:
                return

            collider = entry.getIntoNodePath()

            if collider.hasPythonTag( "owner" ):
                obj = collider.getPythonTag( "owner" )
                if isinstance( obj, Player ):
                    if not trap.ignorePlayer:
                        obj.alterHealth( -1 )
                        trap.ignorePlayer = True
                else:
                    obj.alterHealth( - 10 )

    def updateKeyMap( self, key, state ):
        self.keyMap[ key ] = state

    def update( self, task ):

        dt = globalClock.getDt()

        self.player.update( self.keyMap, dt )
        self.tempEnemy.update( self.player, dt )
        self.tempTrap.update( self.player, dt )

        return task.cont

game = Game()
game.run()
