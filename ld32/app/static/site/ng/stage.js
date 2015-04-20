
angular.module('Stage', [])

//////////////////////////////////////////////////////////////////////////////

.directive('stage',
function()
{
    return {
        restrict: 'AE',
        scope:
        {
            set: '=',
        },
        controllerAs: 'stage',
        controller: function()
        {
            this.puppets = []
        },
        link: function($scope, $element, $attr, ctrl)
        {
            ctrl.set = $scope.set
            $element.css({
                position: 'relative'
            })
        }
    }
})

//////////////////////////////////////////////////////////////////////////////

.directive('puppet',
function()
{
    return {
        restrict: 'AE',
        transclude: true,
        template: '<ng-transclude></ng-transclude>',
        require: [ 'puppet', '^^stage' ],
        scope:
        {
            actor: '=',
            clock: '=',
        },
        conrollerAs: 'puppet',
        controller: function($scope, $element)
        {
        },
        link: function($scope, $element, $attr, requires)
        {
            var ctrl = requires[0]
            ctrl.actor = $scope.actor
            ctrl.stage = requires[1]
            ctrl.set = ctrl.stage.set
            $element.css({
                position: 'absolute'
            })

            $element.addClass('puppet')
            ctrl.actor.enter($scope.clock || ctrl.set.clock)
        }
    }
})

//////////////////////////////////////////////////////////////////////////////

.service('Actor',
function()
{
    function Actor(options)
    {
        options = options || {}
        this.x = this.x0 = options.x0 || 0
        this.y = this.y0 = options.y0 ||  0
        this.width = options.width || 0
        this.height = options.height || 0
        this.move_watchers = []
    }

    Actor.prototype =
    {
        move: function(dx, dy, dt)
        {
            this.x += dx
            this.y += dy

            var alien = this
            angular.forEach(this.move_watchers, function(cb) { cb(alien) })
        },

        move_to: function(x, y)
        {
            if (x instanceof Array)
            {
                this.x = x[0]
                this.y = x[1]
            }
            else if (typeof(x) === 'object')
            {
                this.x = x.x
                this.y = x.y
            }
            else
            {
                this.x = x
                this.y = y
            }

            var alien = this
            angular.forEach(this.move_watchers, function(cb) { cb(alien) })
        },

        enter: function(clock)
        {
        },

        on_moved: function(observer)
        {
            this.move_watchers.push(observer)
        }
    }

    return Actor
})

//////////////////////////////////////////////////////////////////////////////

.service('Set',
function()
{
    return function Set(options)
    {
        options = options || {}
        this.clock = options.clock || new (options)
        this.width = 0
        this.height = 0
    }
})

//////////////////////////////////////////////////////////////////////////////

.service('Clock',
function($interval)
{
    return function Clock(options)
    {
        var clock = this
        options = options || {}
        this.t = options.t0 || 0
        this.running = null
        var notify = []
        var schedule = []

        var then

        function tick()
        {
            var now = Date.now()
            var dt = now - then
            then = now
            
            var t = clock.t += dt

            while(schedule.length)
            {
                var first = schedule[0]
                if (!first.armed)
                {
                    schedule.shift()
                }
                else
                {
                    if (t < first.t)
                    {
                        break
                    }
                    else
                    {
                        schedule.shift()
                        first.fn(t)
                    }
                }
            }

            angular.forEach(notify,
            function(fn)
            {
                fn(t, clock)
            })
        }

        this.play = function(until)
        {
            if (this.running == null)
            {
                then = Date.now()
                this.running = $interval(tick, 30)
            }

            if (until != null)
            {
                this.schedule(function() { clock.pause()}, until)
            }
        }

        this.pause = function()
        {
            if (this.running != null)
            {
                $interval.cancel(this.running)
                this.running = null
            }
        }

        this.schedule = function(fn, dt)
        {
            var scheduled = new Scheduled(fn, clock.t + dt)
            schedule.push(scheduled)
            schedule.sort(function (a,  b) { return a.t - b.t })
            return scheduled
        }

        this.notify = function(fn)
        {
            notify.push(fn)
        }

        this.ignore = function(fn)
        {
            var index = notify.indexOf(fn)
            if (index >= 0)
            {
                notify.splice(index)
            }
        }

        this.reset = function(t0)
        {
            this.pause()
            this.t = t0 || 0
        }

        function Scheduled(fn, t)
        {
            this.armed = true
            this.fn = fn
            this.t = t
        }

        Scheduled.prototype.cancel = function()
        {
            this.armed = false
        }
    }
})

//////////////////////////////////////////////////////////////////////////////

; // End of module
