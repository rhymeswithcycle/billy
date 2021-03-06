billy changelog
===============

1.4.0
-----
**31 August 2012**
    * new summary field on bills
    * enable editing legislators in admin
    * leg_id view replacing more manual_data csvs
    * automatically attempt to link actions to votes and bills
    * support fields API parameter in more places
    * popularity tracking added
    * fix to how roles are shown for old legislators
    * limits to number of items displayed in public view when counts are
        extremely high
    * basic user-account & dev-mode support
    * deeper influence explorer integration
    * addition of import filters
    * ability to create data quality exceptions
    * more tests for models

1.3.0
-----
**30 July 2012**
    * first truly usable version of billy.web.public
    * remove retire, load_legislators, and prune_committees commands in favor of admin
    * more admin improvements including subject support and cleaned up reporting
    * new offices support on legislators
    * refactor of billy.models
    * db: denormalize votes into own collection on bill import
    * db: add action_dates to bills
    * unification of numerous settings into API_KEY
    * bugfix for unicode data in dumpjson
    * bugfix for name matching being too loose from manual_data
    * bugfix for billy-update deleting metadata without --scrape

1.2.0
-----
**29 May 2012**
    * further development of the public site
    * use elasticsearch for bill search
    * improvements to event support
    * refresh of settings
        * ENABLE_OYSTER setting replaces --oyster
        * support for module-specific settings overrides
    * support for a new scrape signature (chambers vs. chamber)
    * utility function for pulling data from .doc files
    * bugfix for pymongo 2.2

1.1.0
-----
**23 April 2012**
    * large refactor of billy.site.{browse,www} into billy.web.{admin,public}
    * require new scrapelib >= 0.7
    * overhaul of event support, greatly improved schema
    * scrape: improved vote validation
    * API: expose internal id on all objects, including bills
    * API: new method for direct lookup of bills by id
    * API: added created_at sort to bills
    * add support for text extraction from bills

1.0.0
-----
**2 April 2012**
    * lots of improvements to billy admin
        * general style overhaul
        * duplicate_versions view
    * API:
        * removal of XML
        * removal of RSS emitter and broken stats endpoint
    * billy-update command line radically changed
        * defaults to actually doing work
        * -vvv dropped
        * --strict dropped, --nostrict now exists
        * simplification of how --session/--term work
    * drop billy-util districtcsv in favor of an admin view
    * previously internal bill ids are now 8 digits
    * addition of billy-update --oyster argument, adds tracking of versions
    * duplicate_versions is now just that, not versions+documents
    * bugfix: stop silently swallowing errors in subject csvs

0.9.6
-----
**27 February 2012**
    * add alternate_bill_ids and related functionality (needed for TN)
    * updated oysterize command to work with oyster >= 0.3
    * added initial work on class-based models
    * added new beginning of web frontend
    * added run logging work
    * bugfix: billy-util broken by jenkins command
    * bugfix: random_bill restricted session

0.9.5
-----
**21 February 2012**
    * added doc_ids on versions and documents
    * API: add boundary_id to legislator responses (experimental)
    * browse: MOM legislator merge tool
    * browse: improved browse templates & random_bill
    * scrapers: --cache_dir argument added
    * scrapers: _partial_vote_bill_id flag added for Rhode Island
    * bugfix: boundary API method returning first polygon
    * bugfix: dotted keys in reports
    * bugfix: billy-util retire
    * bugfix: unicode error in loadlegislators


0.9.4
-----
**20 January 2012**
    * lots of fixes and improvements to browse
        * new /bills/ view
        * row highlighting
        * unmatched_leg_ids page
        * other_actions page
        * json views
        * random_bill/?bad_vote_counts
    * new and fixed utils
        * districtcsv for generating district CSV stubs
        * prunecommittees for removing old committees
        * load_legislators fixed
    * improve session handling
        * session_list in metadata file
        * missing sessions trigger an error
    * new capitol_maps feature in metadata
    * latest_only can be a flag on scrapers that only work for latest term
    * addition of optional mimetype on documents & versions
    * promote legislator's url to a non + field
    * replace all csv usage with unicodecsv
    * API: block requests for over 5000 bills at once


0.9.3
-----
**30 November 2011**
    * force tests to use a test database
    * --mongo_host, --mongo_db, --mongo_port command line options
    * sneaky_update_filter option added, can ignore minor updates
    * API bugfix when chamber isn't specified on bill lookup
    * change importers to use logger instead of unbuffered print statements
    * billy-update
        * billy-scrape deprecated and replaced with billy-update
        * billy-import, billy-bill-scrape, billy-import-districts replaced
    * billy-util
        * takes place of all utility scripts that didn't get merged into billy-update
    * reporting
        * removed billy-generate-stats and replaced with robust reporting
        * updated browse interface to use reports
        * browse interface also got a partial facelift (more to come)

0.9.2
-----
**26 September 2011**
    * documentation improvements/moved to readthedocs.org
    * load settings from a ``billy_settings.py`` file
    * addition of ``SCRAPER_PATHS`` argument

0.9.1
-----
**23 September 2011**
    * packaging bugfix

0.9.0
-----
**23 September 2011**
    * initial release as used by Open States
