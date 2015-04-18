
angular.module('LD32', ['ngRoute', 'ngResource', 'Stage'])

//////////////////////////////////////////////////////////////////////////////

.config([ '$routeProvider',
function($routeProvider)
{
    $routeProvider
        .when('/setup',
        {
            templateUrl: '/static/ld32/ng/tpl/setup.html',
        })
        .when('/playing',
        {
            templateUrl: '/static/ld32/ng/tpl/playing.html',
        })
        .otherwise({
            redirectTo: '/setup'
        })
} ])

//////////////////////////////////////////////////////////////////////////////

.directive('ld32Game', 
function(Set, Actor)
{
    return {
        restrict: 'AE',
        scope:
        {
            into: '=ld32Game',
        },
        controller: function($scope)
        {
            this.set = new Set()
            this.player = new Actor()
            this.monster = new Actor()
        },
        link: function($scope, $element, $attr, ctrl)
        {
            $scope.into = ctrl
        }
    }
})

//////////////////////////////////////////////////////////////////////////////

.directive('ld32Loader',
function()
{
    return {
        restrict: 'AE',
        require: [ '^ld32Game'],
        scope:
        {
            url: '@',
        },
        link: function($scope, $element, $attr, requires)
        {
            console.log(requires)
        }
    }
})

//////////////////////////////////////////////////////////////////////////////

; // End of module

