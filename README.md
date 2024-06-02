# Infokyllti Display Signage System

> [**kyltti**](https://en.wiktionary.org/w/index.php?title=kyltti&oldid=78799674) 🇫🇮
> 1. sign, signpost, signboard 
> 2. plaque

Infokyllti is a Django-based display signage system, which allows the use of a standard web browser as a display signage front-end.

Management of display signage is undertaken using the standard Django administration, and consists of three main objects:

* **Displays**: each display is its own object. Infokyllti keeps track of when displays were last seen.
* **Playlists**: a playlist can be assigned to one or more displays. These keep track of content items to be shown.
* **Content items**: individual items which can be added to playlists. These can be of multiple types (see the `content_items/types` folder for models.)

## Usage
You can run this without much effort using Pipenv or by using the Docker image. This has been tested with an MSSQL database and [Garage](https://garagehq.deuxfleurs.fr/) as an S3-compatible asset storage.

Once you're up and running, navigate to the main URL and a new display will be set up with a randomly-generated persistent ID (stored in a cookie). If, like us, you have displays (for example Smart TVs) that lose cookies, you can set a persistent ID by putting `?config=<YOURIDHERE>` at the end of the URL. 

## Development
The system was developed by Andrew Mathieson (aim29) for Guiseley School. We are releasing this to the community in the hope it can benefit other organisations.

## Thanks
We are indebted to the City of Sault Ste. Marie for their work on their [City Facility TV Displays](https://github.com/cityssm/tv-display) project, which forms the basis of the Infokyllti front-end.