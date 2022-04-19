from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import WindowProperties
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import Vec4, Vec3

class Game( ShowBase ):

    def __init__( self ):

        ShowBase.__init__( self )

        # Configure Window

        properties = WindowProperties()
        properties.setSize( 1000, 750 )
        self.win.requestProperties( properties )

        self.disableMouse()
        self.render.setShaderAuto()

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

        # Actors

        self.tempActor = Actor( "models/PandaChan/act_p3d_chan",
                                { "walk": "models/PandaChan/a_p3d_chan_run"} )
        self.tempActor.reparentTo( self.render )

        # Lights

        ambientLight = AmbientLight( "ambient light" )
        ambientLight.setColor( Vec4( 0.2, 0.2, 0.2, 1 ) )

        self.ambientLightNodePath = self.render.attachNewNode( ambientLight )
        self.render.setLight( self.ambientLightNodePath )

        mainLight = DirectionalLight( "main light" )
        self.mainLightNodePath = self.render.attachNewNode( mainLight )
        self.mainLightNodePath.setHpr( 45, -45, 0 )

        self.render.setLight( self.mainLightNodePath )

        # Panda Chan

        # Position and start animation
        self.tempActor.setPos( 0, 7, 0 )

        self.tempActor.getChild( 0 ).setH( 180 )
        self.tempActor.loop( "walk" )

        # Position camera
        self.camera.setPos( 0, 0, 32 )
        self.camera.setP( -90 )

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

        # Tasks

        self.updateTask = self.taskMgr.add( self.update, "update" )

    def updateKeyMap( self, name, state ):
        self.keyMap[name] = state

    def update( self, task ):

        dt = globalClock.getDt()

        if self.keyMap[ "up" ]:
            self.tempActor.setPos( self.tempActor.getPos() + Vec3( 0, 5.0*dt, 0 ) )
            self.tempActor.getChild( 0 ).setH( 180 )
        if self.keyMap[ "down" ]:
            self.tempActor.setPos( self.tempActor.getPos() + Vec3( 0, -5.0*dt, 0 ) )
            self.tempActor.getChild( 0 ).setH( 0 )
        if self.keyMap[ "left" ]:
            self.tempActor.setPos( self.tempActor.getPos() + Vec3( -5.0*dt, 0, 0 ) )
            self.tempActor.getChild( 0 ).setH( -90 )
        if self.keyMap[ "right" ]:
            self.tempActor.setPos( self.tempActor.getPos() + Vec3( 5.0*dt, 0, 0, ) )
            self.tempActor.getChild( 0 ).setH( 90 )

        if self.keyMap[ "shoot" ]:
            print( "Zap!" )

        return task.cont

game = Game()
game.run()
