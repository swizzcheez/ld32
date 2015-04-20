
angular.module('LD32Game', ['ngRoute', 'ngResource', 'Stage'])

//////////////////////////////////////////////////////////////////////////////

.config([ '$routeProvider',
function($routeProvider)
{
    $routeProvider
        .when('/setup',
        {
            templateUrl: '/static/main/ng/tpl/setup.html',
        })
        .when('/playing',
        {
            templateUrl: '/static/main/ng/tpl/playing.html',
            controller: 'LD32GameCtrl as game',
        })
        .otherwise({
            redirectTo: '/setup'
        })
} ])

//////////////////////////////////////////////////////////////////////////////

.controller('LD32GameCtrl',
function($scope, $http, LD32Arena, Clock, Alien, Shooter)
{
    var game = this
    this.game_id = 1
    this.clock = new Clock()
    this.arena = new LD32Arena({ clock: this.clock })
    this.aliens = []
    this.orders = []
    this.shooter = new Shooter()
    this.running = null
    this.playing = false
    this.won = false
    this.lost = false

    function load(level_url)
    {
        level_url = level_url || game.level_url
        game.level_url = level_url
        $http.get(level_url)
        .success(
        function(level_data)
        {
            game.level = level_data.level
            game.game_id = level_data.game_i
            game.next_level_url = level_data.next_level_url
            game.aliens = []
            game.orders = []
            game.shooter = new Shooter({ 
                aliens: game.aliens,
                on_miss: function() { game.over() },
                on_done: function() { game.beaten() },
            })
            game.running = null
            game.clock.reset()
            //game.clock.schedule(function() { game.over() }, 30000)
            game.playing = true
            game.won = false
            game.lost = false
            angular.forEach(level_data.aliens,
            function(alien)
            {
                game.orders.push({ x: '', y: '' })
                var alien = new Alien(
                {
                    x0: alien.x,
                    y0: alien.y,
                    color: alien.color,
                    fn: eval('(function(t, x0, y0) '  +
                              '{ return ' + alien.formula + '})')
                })
                game.aliens.push(alien)
                alien.on_moved(function(alien)
                {
                    // TODO: Fix this...
                    if (alien.y >= 640)
                    {
                        game.over()
                    }
                })
            })
        })
    }
    $scope.$watch('level_url', load)
    this.reload = load

    this.commit_orders = function()
    {
        this.running = true
        this.shooter.ready(this.orders, this.clock)
        this.clock.play()
    }

    this.over = function()
    {
        this.clock.pause()
        this.playing = false
        this.lost = true
    }

    this.beaten = function()
    {
        this.clock.pause()
        this.playing = false
        this.won = true
    }

    this.next_level = function()
    {
        load(this.next_level_url)
    }
})

//////////////////////////////////////////////////////////////////////////////

.service('LD32Arena',
function(Set)
{
    function LD32Arena(options)
    {
        options = options || {}
        Set.call(this, options)
    }

    angular.extend(LD32Arena.prototype, Set.prototype)
         
    return LD32Arena
})

//////////////////////////////////////////////////////////////////////////////

.service('Shooter',
function(Actor)
{
    function Shooter(options)
    {
        options = options || {}
        Actor.call(this, options)
        this.orders = []
        this.charge = 0
        this.firing = 0
        this.on_miss = options.on_miss
        this.on_done = options.on_done
        this.aliens = options.aliens || []
    }

    angular.extend(Shooter.prototype, Actor.prototype)

    Shooter.prototype.ready = function(orders, clock)
    {
        var shooter = this
        this.order_idx = 0
        this.orders = orders
        var target = this.target = { x:0 , y: 0}
        function ticker(t)
        {
            var current = shooter.orders[shooter.order_idx]

            t /= 1000
            var x = target.x = eval(current.x)
            var y = target.y = eval(current.y)
            t *= 1000

            if (shooter.firing > 0)
            {
                shooter.firing -= 0.05
                shooter.charge -= 0.05
            }
            else
            {
                shooter.charge += Math.random() * 0.03 + 0.02

                if (shooter.charge > 1)
                {
                    shooter.firing = 1.0
                    shooter.charge = 1.0

                    var hit = false
                    angular.forEach(shooter.aliens,
                    function(alien)
                    {
                        var dx = alien.x - x
                        var dy = alien.y - y
                        var d = Math.sqrt(dx * dx + dy * dy)
                        if (!hit && d < 5)
                        {
                            shooter.order_idx++
                            alien.destroy()
                            hit = true
                        }
                    })

                    if (! hit && shooter.on_miss)
                    {
                        shooter.on_miss()
                        clock.ignore(ticker)
                    }
                    else  if (shooter.order_idx >= shooter.orders.length 
                             && shooter.on_done)
                    {
                        shooter.on_done()
                        clock.ignore(ticker)
                    }
                }
            }
        }

        clock.notify(ticker)
    }
         
    return Shooter
})

//////////////////////////////////////////////////////////////////////////////

.service('Alien',
function(Actor)
{
    function Alien(options)
    {
        options = options || {}
        Actor.call(this, options)
        this.fn = options.fn || function(t, x0, y0) { return [ x0, y0 ] }
        this.segments = []
        this.destroyed = false
        this.newSegment()
        this.color = options.color || 'white'
    }

    angular.extend(Alien.prototype, Actor.prototype)

    Alien.prototype.enter = function(clock)
    {
        var alien = this
        var s = 0
        clock.notify(
        function(t)
        {
            if (alien.destooyed)
            {
                clock.ignore(alien)
                return
            }

            alien.move_to(alien.fn.call(alien, t / 1000, alien.x0, alien.y0))
            var ts = parseInt(t / 1000)
            if (ts != s)
            {
                alien.newSegment()
                s = ts
            }
            alien.updateSegment()
        })
    }

    Alien.prototype.newSegment = function()
    {
        var segment = this.segment = { }
        this.segments.push(segment)
        segment.x0 = segment.x1 = this.x
        segment.y0 = segment.y1 = this.y
    }

    Alien.prototype.updateSegment = function()
    {
        var segment = this.segment
        segment.x1 = this.x
        segment.y1 = this.y
    }

    Alien.prototype.destroy = function()
    {
        this.destroyed = true
    }

    return Alien
})

//////////////////////////////////////////////////////////////////////////////

; // End of module

