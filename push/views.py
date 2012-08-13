import urllib2
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from models import FoursquareUser, Venue, Checkin
import simplejson, datetime
from time import sleep
from push.tasks import ping

def home(request):
    return HttpResponseServerError("Use /push dude")

@csrf_exempt
def push(request):
    if request.method == 'POST':
        try:
            # capture JSON data, convert to dictionary
            jsonData = simplejson.loads(request.POST['checkin'])

            # ping the netduino right away
            r = ping.delay()

            # check to see if the user already exists
            try:
                user = FoursquareUser.objects.get(userId = jsonData['user']['id'])

            # if not, then create him!
            except Exception:

                # we have to check since since the twitter field isn't always there
                try:
                    twttr = jsonData['user']['contact']['twitter'],
                except:
                    twttr = None,

                # make the user model
                user = FoursquareUser(
                    userId = jsonData['user']['id'],
                    firstName = jsonData['user']['firstName'],
                    lastName = jsonData['user']['lastName'],
                    photo = jsonData['user']['photo'],
                    gender = jsonData['user']['gender'],
                    homeCity = jsonData['user']['homeCity'],
                    bio = jsonData['user']['bio'],
                    twitter = twttr
                )

                # save dat ish
                user.save()

            # check to see if the venue exists
            try:
                venue = Venue.objects.get(venueId = jsonData['venue']['id'])

            # if not, then create it!
            except Exception:

                # see if the contact stuff exists
                try:
                    phn = jsonData['venue']['contact']['phone']
                except:
                    phn = None
                try:
                    twttr = jsonData['venue']['contact']['twitter']
                except:
                    twttr = None

                # make the venue model
                venue = Venue(
                    venueId = jsonData['venue']['id'],
                    name = jsonData['venue']['name'],
                    phone = phn,
                    twitter = twttr,
                    address = jsonData['venue']['location']['address'],
                    lat = jsonData['venue']['location']['lat'],
                    lng = jsonData['venue']['location']['lng'],
                    postalCode = jsonData['venue']['location']['postalCode'],
                    city = jsonData['venue']['location']['postalCode'],
                    state = jsonData['venue']['location']['state'],
                    country = jsonData['venue']['location']['country'],
                    categoryId = jsonData['venue']['categories'][0]['id'],
                    categoryName = jsonData['venue']['categories'][0]['name'],
                    categoryPluralName = jsonData['venue']['categories'][0]['pluralName'],
                    categoryShortName = jsonData['venue']['categories'][0]['shortName'],
                    categoryIcon = jsonData['venue']['categories'][0]['icon'],
                    categoryPrimary = jsonData['venue']['categories'][0]['primary'],
                    statsCheckinsCount = jsonData['venue']['stats']['checkinsCount'],
                    statsUsersCount = jsonData['venue']['stats']['usersCount'],
                    statsTipsCount = jsonData['venue']['stats']['tipCount'],
                    statsLikesCount = jsonData['venue']['likes']['count'],
                    url = jsonData['venue']['url']
                )

                # save dat ish
                venue.save()

            checkin = Checkin(
                checkinId = jsonData['id'],
                createdAt = datetime.datetime.fromtimestamp(jsonData['createdAt']),
                timezone = jsonData['timeZone'],
                user = user,
                venue = venue
            )
            checkin.save()

            # grab the mayor
            mayorJson = simplejson.loads(urllib2.urlopen(
                "https://api.foursquare.com/v2/venues/" +
                jsonData['venue']['id'] +
                "?oauth_token=Y10QHO1ZKLBPAXKUZPKSHBFW5WVRKURG0S2CKBX2LA04ERZS&v=20120608").read()
            )

            mayorId = mayorJson['response']['venue']['mayor']['user']['id']

            # check to see if mayor is in DB, if not then add it
            try:
                mayor = FoursquareUser.objects.get(userId = mayorId)
                venue.mayor = mayor
            except:

                # we have to check since since the twitter field isn't always there
                try:
                    twttr = mayorJson['response']['venue']['mayor']['user']['contact']['twitter'],
                except:
                    twttr = None,

                user = FoursquareUser(
                    userId = mayorJson['response']['venue']['mayor']['user']['id'],
                    firstName = mayorJson['response']['venue']['mayor']['user']['firstName'],
                    lastName = mayorJson['response']['venue']['mayor']['user']['lastName'],
                    photo = mayorJson['response']['venue']['mayor']['user']['photo'],
                    gender = mayorJson['response']['venue']['mayor']['user']['gender'],
                    homeCity = mayorJson['response']['venue']['mayor']['user']['homeCity'],
                    bio = mayorJson['response']['venue']['mayor']['user']['bio'],
                    twitter = twttr
                )

                # save dat ish
                user.save()

            venue.mayor = user

            return HttpResponse("OK\r\n")
        except Exception as steve:
            return HttpResponseServerError("ERROR" + " " + steve.message + "\r\n")
        finally:
            print r.status
    else:
        return HttpResponseServerError("Push some ish and get back to me\r\n")
