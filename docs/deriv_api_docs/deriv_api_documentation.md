# Compiled Deriv API Documentation



---

## Documentation from [https://api.deriv.com/](https://api.deriv.com/)

Skip to main content

[![Deriv API logo](/img/derivlogo.svg)](/)[API explorer](/api-
explorer)[Documentation](https://developers.deriv.com)[Deriv
tech](https://tech.deriv.com/)[Bug
bounty](https://hackerone.com/deriv?type=team)

Log inSign up

EN

  * English
  * Français

# Deriv API

Use our powerful, flexible, and free API to build a custom trading  
platform - for yourself or for your business.

[Quick Start](https://developers.deriv.com)

![](/img/js-library.svg)

## Comprehensive all-in-one  
client library

Simplify your development processes and get your app up and running  
faster with the client library of your choice.

[![](/img/js.svg)Go to the JavaScript library![](/img/library-
chevron.svg)](https://deriv-com.github.io/deriv-api/)

[![](/img/py.svg)Go to the Python library![](/img/library-
chevron.svg)](https://deriv-com.github.io/python-deriv-api/)

[![](/img/flutter.svg)Go to the Flutter library![](/img/library-
chevron.svg)](https://github.com/deriv-com/flutter-deriv-api)

## Benefits of using Deriv API

![automation](/img/automation.svg)Automation![integration](/img/integration.svg)Easy
integration![execution](/img/execution.svg)Fast execution![A trading app
created using Deriv API shown on a laptop.](/img/personalisation.png)

### Personalise your trading

Personalise your trading apps to match your needs. Create charts and views the
way you like them. Develop your trading app using any common programming
language and extend your trading opportunities.

![A business man testing the Deriv API for his trading app.](/img/build-
business.png)

### Build a business and earn more

Create your own trading apps by taking advantage of the power of Deriv's
trading services. Share your apps with fellow traders or customers, and get a
chance to earn more or build your own business.

## Ways to earn with Deriv API

![](/img/checklist-icon-red.svg)

Register your app with Deriv, and add a percentage markup to the contract
prices to profit from every purchased contract.

![](/img/checklist-icon-red.svg)

Sign up as an affiliate, build your app, and get commissions on trades
completed via your app and the affiliate plan you select.

![](/img/checklist-icon-red.svg)

Sign up as a payment agent, build your own custom payment website, and use our
API to earn commission on every payment you process for Deriv's clients.

## Get started with our API in 3 simple steps:

[![](/img/guide.svg)1\. Learn about our APIUnderstand basic concepts and
terminologies![](img/home-
arrow.svg)](https://developers.deriv.com)[![](/img/sign-up.svg)2\. Sign
upCreate a free Deriv account to access our API![](img/home-
arrow.svg)](https://deriv.com/signup/)[![](/img/register-your-app.svg)3\.
Register your appFill out the registration form to start using Deriv
API![](img/home-arrow.svg)](/dashboard)By using our API, you confirm that you
have read and agreed to our[ terms and
conditions.](https://deriv.com/tnc/business-partners-api-user.pdf)

## Deriv API features

Deriv API gives you full access to all the trading functionalities of DTrader
and allows you to build your own comprehensive trading systems and analysis
tools.

With our API, you'll be able to:

  * ![](/img/checklist-icon-grey.svg)

Trade digital options and multipliers

  * ![](/img/checklist-icon-grey.svg)

Monitor real-time pricing

  * ![](/img/checklist-icon-grey.svg)

Buy/sell contracts

  * ![](/img/checklist-icon-grey.svg)

Manage user's accounts

  * ![](/img/checklist-icon-grey.svg)

Monitor existing contracts

  * ![](/img/checklist-icon-grey.svg)

View user's historical transactions

![Using Deriv API to build a trading app with features like real-time pricing
charts available on Dtrader.](/img/api-featutes.png)

###### API

  * [Dashboard](/dashboard)
  * [API explorer](/api-explorer)
  * [Documentation](https://developers.deriv.com)
  * [Deriv Tech](https://deriv.com/derivtech)
  * [Bug bounty](https://hackerone.com/deriv?type=team)

###### Deriv.com

  * [Homepage](https://deriv.com/)
  * [Who we are](https://deriv.com/who-we-are)
  * [Contact us](https://deriv.com/contact-us)

### API

### Deriv.com

##### Get connected

Discuss ideas and share solutions with developers worldwide.

Join our communityTelegram

##### We're here to help

Email us at

[api-support@deriv.com ](mailto:api-support@deriv.com)

if you need any assistance or support.

Send an email



---

## Documentation from [https://deriv-com.github.io/python-deriv-api/](https://deriv-com.github.io/python-deriv-api/)

# Package `deriv_api`

# python-deriv-api

A python implementation of deriv api library.

[![PyPI](https://img.shields.io/pypi/v/python_deriv_api.svg?style=flat-
square)](https://pypi.org/project/python_deriv_api/) [![Python
3.9.6](https://img.shields.io/badge/python-3.9.6-blue.svg)](https://www.python.org/download/releases/3.9.6/)
[![Test status](https://github.com/deriv-com/python-deriv-
api/actions/workflows/build.yml/badge.svg)](https://github.com/deriv-
com/python-deriv-api)

Go through [api.deriv.com](https://api.deriv.com/) to know simple easy steps
on how to register and get access. Use this all-in-one python library to set
up and make your app running or you can extend it.

### Requirement

Python (3.9.6 or higher is recommended) and pip3

Note: There is bug in 'websockets' package with python 3.9.7, hope that will
be fixed in 3.9.8 as mentioned in
<https://github.com/aaugustin/websockets/issues/1051.> Please exclude python
3.9.7.

# Installation

`python3 -m pip install python_deriv_api`

# Usage

This is basic deriv-api python library which helps to make websockets
connection and deal the API calls (including subscription).

Import the module

    
    
    from deriv_api import DerivAPI
    

Access

    
    
    api = DerivAPI(endpoint='ws://...', app_id=1234);
    response = await api.ping({'ping': 1})
    print(response) 
    

## Creating a websockets connection and API instantiation

You can either create an instance of websockets and pass it as connection or
pass the endpoint and app_id to the constructor to create the connection for
you.

If you pass the connection it's up to you to reconnect in case the connection
drops (cause API doesn't know how to create the same connection).

  * Pass the arguments needed to create a connection:

    
    
       api = DerivAPI(endpoint='ws://...', app_id=1234);
    

  * create and use a previously opened connection:

    
    
       connection = await websockets.connect('ws://...')
       api = DerivAPI(connection=connection)
    

# Documentation

#### API reference

The complete API reference is hosted [here](https://deriv-
com.github.io/python-deriv-api/)

Examples [here](https://github.com/deriv-com/python-deriv-
api/tree/master/examples)

# Development

    
    
    git clone https://github.com/deriv-com/python-deriv-api
    cd python-deriv-api
    

Setup environment

    
    
    make setup
    

Setup environment and run test

    
    
    make all
    

#### Run test

    
    
    python setup.py pytest
    

or

    
    
    pytest
    

or

    
    
    make test
    

#### Generate documentations

Generate html version of the docs and publish it to gh-pages

    
    
    make gh-pages
    

#### Build the package

    
    
    make build
    

#### Run examples

set token and run example

    
    
    export DERIV_TOKEN=xxxTokenxxx
    PYTHONPATH=. python3 examples/simple_bot1.py
    

# Usage examples

## Short examples

    
    
        from deriv_api import DerivAPI
        api = DerivAPI(app_id=app_id)
    

### Authenticate to an account using token

    
    
        authorize = await api.authorize(api_token)
        print(authorize)
    

### Get Balance

    
    
        account = await api.balance()
        print(account) 
    

### Get all the assets info

    
    
        assets = await api.asset_index({"asset_index": 1})
        print(assets)
    

To get assets info from cache

    
    
        assets = await api.cache.asset_index({"asset_index": 1})
        print(assets)
    

### Get all active symbols

    
    
        active_symbols = await api.active_symbols({"active_symbols": "full"})
        print(active_symbols)
    

To get active symbols from cache

    
    
        active_symbols = await api.cache.active_symbols({"active_symbols": "full"})
        print(active_symbols)
    

### Get proposal

    
    
        proposal = await api.proposal({"proposal": 1, "amount": 100, "barrier": "+0.1", "basis": "payout",
                                       "contract_type": "CALL", "currency": "USD", "duration": 60, "duration_unit": "s",
                                       "symbol": "R_100"
        })
        print(proposal) 
    

subscribe the proposal stream

    
    
        source_proposal: Observable = await api.subscribe({"proposal": 1, "amount": 100, "barrier": "+0.1", "basis": "payout",
                                               "contract_type": "CALL", "currency": "USD", "duration": 160,
                                               "duration_unit": "s",
                                               "symbol": "R_100",
                                               "subscribe": 1
                                               })
        source_proposal.subscribe(lambda proposal: print(proposal))
    

### Buy

    
    
        proposal_id = proposal.get('proposal').get('id')
        buy = await api.buy({"buy": proposal_id, "price": 100})
        print(buy)
    

### open contract detail

    
    
        contract_id = buy.get('buy').get('contract_id')
        poc = await api.proposal_open_contract(
            {"proposal_open_contract": 1, "contract_id": contract_id })
        print(poc)
    

subscribe the open contract stream

    
    
        source_poc: Observable = await api.subscribe({"proposal_open_contract": 1, "contract_id": contract_id})
        source_poc.subscribe(lambda poc: print(poc)
    

### Sell

    
    
        contract_id = buy.get('buy').get('contract_id')
        sell = await api.sell({"sell": contract_id, "price": 40})
        print(sell)
    

### Profit table

    
    
        profit_table = await api.profit_table({"profit_table": 1, "description": 1, "sort": "ASC"})
        print(profit_table)
    

### Transaction statement

    
    
        statement = await api.statement({"statement": 1, "description": 1, "limit": 100, "offset": 25})
        print(statement)
    

### Subscribe a stream

We are using rxpy to maintain our deriv api subscriptions. Please distinguish
api subscription from rxpy sequence subscription

    
    
        # creating a rxpy sequence object to represent deriv api streams
        source_tick_50 = await api.subscribe({'ticks': 'R_50'})
    
        # subscribe the rxpy sequence with a callback function,
        # when the data received, the call back function will be called
        source_tick_50.subscribe(lambda tick: print(tick))
    

### unsubscribe the rxpy sequence

    
    
        seq_sub = source_tick_50.subscribe(lambda tick: print(tick))
        seq_sub.dispose()
    

### unsubscribe the deriv api stream

There are 2 ways to unsubscribe deriv api stream

  * by `dispose` all sequence subscriptions

    
    
        # creating a rxpy sequence object to represent deriv api streams
        source_tick_50 = await api.subscribe({'ticks': 'R_50'})
        # subscribe the rxpy sequence with a callback function,
        # when the data received , the call back function will be called
        seq_sub1 = source_tick_50.subscribe(lambda tick: print(f"get tick from sub1 {tick}"))
        seq_sub2 = source_tick_50.subscribe(lambda tick: print(f"get tick from sub2 {tick}"))
        seq_sub1.dispose()
        seq_sub2.dispose()
        # When all seq subscriptions of one sequence are disposed. Then a `forget` will be called and that deriv api stream will be unsubscribed
    

  * by `forget` that deriv stream

    
    
        # get a datum first
        from rx import operators as op
        tick = await source_tick_50.pipe(op.first(), op.to_future)
        api.forget(tick['R_50']['subscription']['id'])
    

### print errors

    
    
        api.sanity_errors.subscribe(lambda err: print(err))
    

### do something when one type of message coming

    
    
        async def print_hello_after_authorize():
            auth_data = await api.expect_response('authorize')
            print(f"Hello {auth_data['authorize']['fullname']}")
        asyncio.create_task(print_hello_after_authorize())
        api.authorize({'authorize': 'AVALIDTOKEN'})
    

## Sub-modules

`[deriv_api.cache](cache.html "deriv_api.cache")`

    

`[deriv_api.deriv_api](deriv_api.html "deriv_api.deriv_api")`

    

`[deriv_api.deriv_api_calls](deriv_api_calls.html
"deriv_api.deriv_api_calls")`

    

`[deriv_api.in_memory](in_memory.html "deriv_api.in_memory")`

    

`[deriv_api.middlewares](middlewares.html "deriv_api.middlewares")`

    

`[deriv_api.streams_list](streams_list.html "deriv_api.streams_list")`

    

`[deriv_api.subscription_manager](subscription_manager.html
"deriv_api.subscription_manager")`

    

# Index

  * python-deriv-api
    * Requirement
  * Installation
  * Usage
    * Creating a websockets connection and API instantiation
  * Documentation
    * API reference
  * Development
    * Run test
    * Generate documentations
    * Build the package
    * Run examples
  * Usage examples
    * Short examples
      * Authenticate to an account using token
      * Get Balance
      * Get all the assets info
      * Get all active symbols
      * Get proposal
      * Buy
      * open contract detail
      * Sell
      * Profit table
      * Transaction statement
      * Subscribe a stream
      * unsubscribe the rxpy sequence
      * unsubscribe the deriv api stream
      * print errors
      * do something when one type of message coming

  * ### Sub-modules

    * `[deriv_api.cache](cache.html "deriv_api.cache")`
    * `[deriv_api.deriv_api](deriv_api.html "deriv_api.deriv_api")`
    * `[deriv_api.deriv_api_calls](deriv_api_calls.html "deriv_api.deriv_api_calls")`
    * `[deriv_api.in_memory](in_memory.html "deriv_api.in_memory")`
    * `[deriv_api.middlewares](middlewares.html "deriv_api.middlewares")`
    * `[deriv_api.streams_list](streams_list.html "deriv_api.streams_list")`
    * `[deriv_api.subscription_manager](subscription_manager.html "deriv_api.subscription_manager")`

Generated by [pdoc 0.10.0](https://pdoc3.github.io/pdoc "pdoc: Python API
documentation generator").



---

## Documentation from [https://deriv-com.github.io/python-deriv-api/cache.html](https://deriv-com.github.io/python-deriv-api/cache.html)

# Module `deriv_api.cache`

## Classes

` class Cache (api, storage) `

    

Cache - A class for implementing in-memory and persistent cache

The real implementation of the underlying cache is delegated to the storage
object (See the params).

The storage object needs to implement the API.

## Examples

  * Read the latest active symbols

    
    
    >>> symbols = await api.active_symbols()
    

  * Read the data from cache if available

    
    
    >>> cached_symbols = await api.cache.active_symbols()
    

## Parameters

    
    
    api : deriv_api.DerivAPI
        API instance to get data that is not cached
    storage : Object
        A storage instance to use for caching
    

### Ancestors

  * [DerivAPICalls](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls "deriv_api.deriv_api_calls.DerivAPICalls")

### Inherited members

  * `**[DerivAPICalls](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls "deriv_api.deriv_api_calls.DerivAPICalls")**`: 
    * `[active_symbols](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.active_symbols "deriv_api.deriv_api_calls.DerivAPICalls.active_symbols")`
    * `[api_token](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.api_token "deriv_api.deriv_api_calls.DerivAPICalls.api_token")`
    * `[app_delete](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.app_delete "deriv_api.deriv_api_calls.DerivAPICalls.app_delete")`
    * `[app_get](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.app_get "deriv_api.deriv_api_calls.DerivAPICalls.app_get")`
    * `[app_list](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.app_list "deriv_api.deriv_api_calls.DerivAPICalls.app_list")`
    * `[app_markup_details](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.app_markup_details "deriv_api.deriv_api_calls.DerivAPICalls.app_markup_details")`
    * `[app_markup_statistics](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.app_markup_statistics "deriv_api.deriv_api_calls.DerivAPICalls.app_markup_statistics")`
    * `[app_register](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.app_register "deriv_api.deriv_api_calls.DerivAPICalls.app_register")`
    * `[app_update](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.app_update "deriv_api.deriv_api_calls.DerivAPICalls.app_update")`
    * `[asset_index](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.asset_index "deriv_api.deriv_api_calls.DerivAPICalls.asset_index")`
    * `[authorize](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.authorize "deriv_api.deriv_api_calls.DerivAPICalls.authorize")`
    * `[balance](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.balance "deriv_api.deriv_api_calls.DerivAPICalls.balance")`
    * `[buy](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.buy "deriv_api.deriv_api_calls.DerivAPICalls.buy")`
    * `[buy_contract_for_multiple_accounts](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.buy_contract_for_multiple_accounts "deriv_api.deriv_api_calls.DerivAPICalls.buy_contract_for_multiple_accounts")`
    * `[cancel](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.cancel "deriv_api.deriv_api_calls.DerivAPICalls.cancel")`
    * `[cashier](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.cashier "deriv_api.deriv_api_calls.DerivAPICalls.cashier")`
    * `[contract_update](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.contract_update "deriv_api.deriv_api_calls.DerivAPICalls.contract_update")`
    * `[contract_update_history](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.contract_update_history "deriv_api.deriv_api_calls.DerivAPICalls.contract_update_history")`
    * `[contracts_for](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.contracts_for "deriv_api.deriv_api_calls.DerivAPICalls.contracts_for")`
    * `[copy_start](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.copy_start "deriv_api.deriv_api_calls.DerivAPICalls.copy_start")`
    * `[copy_stop](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.copy_stop "deriv_api.deriv_api_calls.DerivAPICalls.copy_stop")`
    * `[copytrading_list](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.copytrading_list "deriv_api.deriv_api_calls.DerivAPICalls.copytrading_list")`
    * `[copytrading_statistics](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.copytrading_statistics "deriv_api.deriv_api_calls.DerivAPICalls.copytrading_statistics")`
    * `[crypto_config](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.crypto_config "deriv_api.deriv_api_calls.DerivAPICalls.crypto_config")`
    * `[document_upload](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.document_upload "deriv_api.deriv_api_calls.DerivAPICalls.document_upload")`
    * `[economic_calendar](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.economic_calendar "deriv_api.deriv_api_calls.DerivAPICalls.economic_calendar")`
    * `[exchange_rates](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.exchange_rates "deriv_api.deriv_api_calls.DerivAPICalls.exchange_rates")`
    * `[forget](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.forget "deriv_api.deriv_api_calls.DerivAPICalls.forget")`
    * `[forget_all](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.forget_all "deriv_api.deriv_api_calls.DerivAPICalls.forget_all")`
    * `[get_account_status](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.get_account_status "deriv_api.deriv_api_calls.DerivAPICalls.get_account_status")`
    * `[get_financial_assessment](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.get_financial_assessment "deriv_api.deriv_api_calls.DerivAPICalls.get_financial_assessment")`
    * `[get_limits](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.get_limits "deriv_api.deriv_api_calls.DerivAPICalls.get_limits")`
    * `[get_self_exclusion](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.get_self_exclusion "deriv_api.deriv_api_calls.DerivAPICalls.get_self_exclusion")`
    * `[get_settings](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.get_settings "deriv_api.deriv_api_calls.DerivAPICalls.get_settings")`
    * `[identity_verification_document_add](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.identity_verification_document_add "deriv_api.deriv_api_calls.DerivAPICalls.identity_verification_document_add")`
    * `[kyc_auth_status](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.kyc_auth_status "deriv_api.deriv_api_calls.DerivAPICalls.kyc_auth_status")`
    * `[landing_company](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.landing_company "deriv_api.deriv_api_calls.DerivAPICalls.landing_company")`
    * `[landing_company_details](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.landing_company_details "deriv_api.deriv_api_calls.DerivAPICalls.landing_company_details")`
    * `[login_history](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.login_history "deriv_api.deriv_api_calls.DerivAPICalls.login_history")`
    * `[logout](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.logout "deriv_api.deriv_api_calls.DerivAPICalls.logout")`
    * `[mt5_deposit](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.mt5_deposit "deriv_api.deriv_api_calls.DerivAPICalls.mt5_deposit")`
    * `[mt5_get_settings](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.mt5_get_settings "deriv_api.deriv_api_calls.DerivAPICalls.mt5_get_settings")`
    * `[mt5_login_list](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.mt5_login_list "deriv_api.deriv_api_calls.DerivAPICalls.mt5_login_list")`
    * `[mt5_new_account](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.mt5_new_account "deriv_api.deriv_api_calls.DerivAPICalls.mt5_new_account")`
    * `[mt5_password_change](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.mt5_password_change "deriv_api.deriv_api_calls.DerivAPICalls.mt5_password_change")`
    * `[mt5_password_check](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.mt5_password_check "deriv_api.deriv_api_calls.DerivAPICalls.mt5_password_check")`
    * `[mt5_password_reset](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.mt5_password_reset "deriv_api.deriv_api_calls.DerivAPICalls.mt5_password_reset")`
    * `[mt5_withdrawal](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.mt5_withdrawal "deriv_api.deriv_api_calls.DerivAPICalls.mt5_withdrawal")`
    * `[new_account_maltainvest](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.new_account_maltainvest "deriv_api.deriv_api_calls.DerivAPICalls.new_account_maltainvest")`
    * `[new_account_real](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.new_account_real "deriv_api.deriv_api_calls.DerivAPICalls.new_account_real")`
    * `[new_account_virtual](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.new_account_virtual "deriv_api.deriv_api_calls.DerivAPICalls.new_account_virtual")`
    * `[oauth_apps](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.oauth_apps "deriv_api.deriv_api_calls.DerivAPICalls.oauth_apps")`
    * `[p2p_advert_create](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advert_create "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advert_create")`
    * `[p2p_advert_info](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advert_info "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advert_info")`
    * `[p2p_advert_list](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advert_list "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advert_list")`
    * `[p2p_advert_update](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advert_update "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advert_update")`
    * `[p2p_advertiser_adverts](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_adverts "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_adverts")`
    * `[p2p_advertiser_create](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_create "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_create")`
    * `[p2p_advertiser_info](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_info "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_info")`
    * `[p2p_advertiser_list](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_list "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_list")`
    * `[p2p_advertiser_payment_methods](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_payment_methods "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_payment_methods")`
    * `[p2p_advertiser_relations](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_relations "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_relations")`
    * `[p2p_advertiser_update](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_update "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_update")`
    * `[p2p_chat_create](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_chat_create "deriv_api.deriv_api_calls.DerivAPICalls.p2p_chat_create")`
    * `[p2p_order_cancel](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_cancel "deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_cancel")`
    * `[p2p_order_confirm](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_confirm "deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_confirm")`
    * `[p2p_order_create](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_create "deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_create")`
    * `[p2p_order_dispute](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_dispute "deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_dispute")`
    * `[p2p_order_info](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_info "deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_info")`
    * `[p2p_order_list](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_list "deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_list")`
    * `[p2p_order_review](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_review "deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_review")`
    * `[p2p_payment_methods](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_payment_methods "deriv_api.deriv_api_calls.DerivAPICalls.p2p_payment_methods")`
    * `[p2p_ping](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_ping "deriv_api.deriv_api_calls.DerivAPICalls.p2p_ping")`
    * `[payment_methods](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.payment_methods "deriv_api.deriv_api_calls.DerivAPICalls.payment_methods")`
    * `[paymentagent_create](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_create "deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_create")`
    * `[paymentagent_details](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_details "deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_details")`
    * `[paymentagent_list](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_list "deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_list")`
    * `[paymentagent_transfer](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_transfer "deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_transfer")`
    * `[paymentagent_withdraw](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_withdraw "deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_withdraw")`
    * `[paymentagent_withdraw_justification](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_withdraw_justification "deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_withdraw_justification")`
    * `[payout_currencies](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.payout_currencies "deriv_api.deriv_api_calls.DerivAPICalls.payout_currencies")`
    * `[ping](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.ping "deriv_api.deriv_api_calls.DerivAPICalls.ping")`
    * `[portfolio](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.portfolio "deriv_api.deriv_api_calls.DerivAPICalls.portfolio")`
    * `[profit_table](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.profit_table "deriv_api.deriv_api_calls.DerivAPICalls.profit_table")`
    * `[proposal](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.proposal "deriv_api.deriv_api_calls.DerivAPICalls.proposal")`
    * `[proposal_open_contract](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.proposal_open_contract "deriv_api.deriv_api_calls.DerivAPICalls.proposal_open_contract")`
    * `[reality_check](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.reality_check "deriv_api.deriv_api_calls.DerivAPICalls.reality_check")`
    * `[residence_list](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.residence_list "deriv_api.deriv_api_calls.DerivAPICalls.residence_list")`
    * `[revoke_oauth_app](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.revoke_oauth_app "deriv_api.deriv_api_calls.DerivAPICalls.revoke_oauth_app")`
    * `[sell](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.sell "deriv_api.deriv_api_calls.DerivAPICalls.sell")`
    * `[sell_contract_for_multiple_accounts](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.sell_contract_for_multiple_accounts "deriv_api.deriv_api_calls.DerivAPICalls.sell_contract_for_multiple_accounts")`
    * `[sell_expired](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.sell_expired "deriv_api.deriv_api_calls.DerivAPICalls.sell_expired")`
    * `[set_account_currency](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.set_account_currency "deriv_api.deriv_api_calls.DerivAPICalls.set_account_currency")`
    * `[set_financial_assessment](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.set_financial_assessment "deriv_api.deriv_api_calls.DerivAPICalls.set_financial_assessment")`
    * `[set_self_exclusion](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.set_self_exclusion "deriv_api.deriv_api_calls.DerivAPICalls.set_self_exclusion")`
    * `[set_settings](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.set_settings "deriv_api.deriv_api_calls.DerivAPICalls.set_settings")`
    * `[statement](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.statement "deriv_api.deriv_api_calls.DerivAPICalls.statement")`
    * `[states_list](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.states_list "deriv_api.deriv_api_calls.DerivAPICalls.states_list")`
    * `[ticks](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.ticks "deriv_api.deriv_api_calls.DerivAPICalls.ticks")`
    * `[ticks_history](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.ticks_history "deriv_api.deriv_api_calls.DerivAPICalls.ticks_history")`
    * `[time](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.time "deriv_api.deriv_api_calls.DerivAPICalls.time")`
    * `[tnc_approval](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.tnc_approval "deriv_api.deriv_api_calls.DerivAPICalls.tnc_approval")`
    * `[topup_virtual](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.topup_virtual "deriv_api.deriv_api_calls.DerivAPICalls.topup_virtual")`
    * `[trading_durations](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.trading_durations "deriv_api.deriv_api_calls.DerivAPICalls.trading_durations")`
    * `[trading_platform_investor_password_reset](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.trading_platform_investor_password_reset "deriv_api.deriv_api_calls.DerivAPICalls.trading_platform_investor_password_reset")`
    * `[trading_platform_password_reset](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.trading_platform_password_reset "deriv_api.deriv_api_calls.DerivAPICalls.trading_platform_password_reset")`
    * `[trading_servers](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.trading_servers "deriv_api.deriv_api_calls.DerivAPICalls.trading_servers")`
    * `[trading_times](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.trading_times "deriv_api.deriv_api_calls.DerivAPICalls.trading_times")`
    * `[transaction](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.transaction "deriv_api.deriv_api_calls.DerivAPICalls.transaction")`
    * `[transfer_between_accounts](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.transfer_between_accounts "deriv_api.deriv_api_calls.DerivAPICalls.transfer_between_accounts")`
    * `[unsubscribe_email](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.unsubscribe_email "deriv_api.deriv_api_calls.DerivAPICalls.unsubscribe_email")`
    * `[verify_email](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.verify_email "deriv_api.deriv_api_calls.DerivAPICalls.verify_email")`
    * `[verify_email_cellxpert](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.verify_email_cellxpert "deriv_api.deriv_api_calls.DerivAPICalls.verify_email_cellxpert")`
    * `[website_status](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.website_status "deriv_api.deriv_api_calls.DerivAPICalls.website_status")`

# Index

  * ### Super-module

    * `[deriv_api](index.html "deriv_api")`
  * ### Classes

    * #### `Cache`

Generated by [pdoc 0.10.0](https://pdoc3.github.io/pdoc "pdoc: Python API
documentation generator").



---

## Documentation from [https://deriv-com.github.io/python-deriv-api/deriv_api.html](https://deriv-com.github.io/python-deriv-api/deriv_api.html)

# Module `deriv_api.deriv_api`

## Classes

` class DerivAPI (**options) `

    

The minimum functionality provided by DerivAPI, provides direct calls to the
API. `api.cache` is available if you want to use the cached data

## Examples

  * Pass the arguments needed to create a connection:

    
    
    >>> api = DerivAPI(endpoint='ws://...', app_id=1234)
    

  * create and use a previously opened connection:

    
    
    >>> connection = await websockets.connect('ws://...')
    >>> api = DerivAPI(connection=connection)
    

## Parameters

    
    
    options : dict with following keys
        connection : websockets.WebSocketClientProtocol
            A ready to use connection
        endpoint : String
            API server to connect to
        app_id : String
            Application ID of the API user
        lang : String
            Language of the API communication
        brand : String
            Brand name
        middleware : MiddleWares
            middlewares to call on certain API actions. Now two middlewares are supported: sendWillBeCalled and
            sendIsCalled
    

## Properties

cache: Cache Temporary cache default to InMemory storage : Cache If specified,
uses a more persistent cache (local storage, etc.) events: Observable An
Observable object that will send data when events like 'connect', 'send',
'message' happen

### Ancestors

  * [DerivAPICalls](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls "deriv_api.deriv_api_calls.DerivAPICalls")

### Methods

` async def subscribe(self, request) `

    

Subscribe to a given request

## Parameters

    
    
    request : dict
        Subscribe request
    

## Example

    
    
    >>> proposal_subscription = api.subscribe({"proposal_open_contract": 1, "contract_id": 11111111, "subscribe": 1})
    

## Returns

    
    
    Observable
    

` async def forget(self, subs_id) `

    

Forget / unsubscribe the specific subscription.

## Parameters

    
    
    subs_id : str
        subscription id
    

## Returns

    
    
    Returns dict
    

` async def forget_all(self, *types) `

    

Forget / unsubscribe the subscriptions of given types.

Possible values are: 'ticks', 'candles', 'proposal', 'proposal_open_contract',
'balance', 'transaction'

## Parameter

    
    
    *types : Any number of non-keyword arguments
    

## Example

    
    
    api.forget_all("ticks", "candles")
    

## Returns

    
    
    Returns the dict
    

` def expect_response(self, *msg_types) `

    

Expect specific message types

## Parameters

    
    
    *msg_types : variable number of non-key string argument
        Expect these types to be received by the API
    

## Returns

    
    
     Resolves to a single response or an array
    

` async def clear(self) `

    

Disconnect and cancel all the tasks

### Inherited members

  * `**[DerivAPICalls](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls "deriv_api.deriv_api_calls.DerivAPICalls")**`: 
    * `[active_symbols](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.active_symbols "deriv_api.deriv_api_calls.DerivAPICalls.active_symbols")`
    * `[api_token](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.api_token "deriv_api.deriv_api_calls.DerivAPICalls.api_token")`
    * `[app_delete](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.app_delete "deriv_api.deriv_api_calls.DerivAPICalls.app_delete")`
    * `[app_get](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.app_get "deriv_api.deriv_api_calls.DerivAPICalls.app_get")`
    * `[app_list](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.app_list "deriv_api.deriv_api_calls.DerivAPICalls.app_list")`
    * `[app_markup_details](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.app_markup_details "deriv_api.deriv_api_calls.DerivAPICalls.app_markup_details")`
    * `[app_markup_statistics](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.app_markup_statistics "deriv_api.deriv_api_calls.DerivAPICalls.app_markup_statistics")`
    * `[app_register](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.app_register "deriv_api.deriv_api_calls.DerivAPICalls.app_register")`
    * `[app_update](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.app_update "deriv_api.deriv_api_calls.DerivAPICalls.app_update")`
    * `[asset_index](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.asset_index "deriv_api.deriv_api_calls.DerivAPICalls.asset_index")`
    * `[authorize](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.authorize "deriv_api.deriv_api_calls.DerivAPICalls.authorize")`
    * `[balance](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.balance "deriv_api.deriv_api_calls.DerivAPICalls.balance")`
    * `[buy](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.buy "deriv_api.deriv_api_calls.DerivAPICalls.buy")`
    * `[buy_contract_for_multiple_accounts](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.buy_contract_for_multiple_accounts "deriv_api.deriv_api_calls.DerivAPICalls.buy_contract_for_multiple_accounts")`
    * `[cancel](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.cancel "deriv_api.deriv_api_calls.DerivAPICalls.cancel")`
    * `[cashier](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.cashier "deriv_api.deriv_api_calls.DerivAPICalls.cashier")`
    * `[contract_update](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.contract_update "deriv_api.deriv_api_calls.DerivAPICalls.contract_update")`
    * `[contract_update_history](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.contract_update_history "deriv_api.deriv_api_calls.DerivAPICalls.contract_update_history")`
    * `[contracts_for](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.contracts_for "deriv_api.deriv_api_calls.DerivAPICalls.contracts_for")`
    * `[copy_start](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.copy_start "deriv_api.deriv_api_calls.DerivAPICalls.copy_start")`
    * `[copy_stop](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.copy_stop "deriv_api.deriv_api_calls.DerivAPICalls.copy_stop")`
    * `[copytrading_list](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.copytrading_list "deriv_api.deriv_api_calls.DerivAPICalls.copytrading_list")`
    * `[copytrading_statistics](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.copytrading_statistics "deriv_api.deriv_api_calls.DerivAPICalls.copytrading_statistics")`
    * `[crypto_config](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.crypto_config "deriv_api.deriv_api_calls.DerivAPICalls.crypto_config")`
    * `[document_upload](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.document_upload "deriv_api.deriv_api_calls.DerivAPICalls.document_upload")`
    * `[economic_calendar](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.economic_calendar "deriv_api.deriv_api_calls.DerivAPICalls.economic_calendar")`
    * `[exchange_rates](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.exchange_rates "deriv_api.deriv_api_calls.DerivAPICalls.exchange_rates")`
    * `[get_account_status](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.get_account_status "deriv_api.deriv_api_calls.DerivAPICalls.get_account_status")`
    * `[get_financial_assessment](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.get_financial_assessment "deriv_api.deriv_api_calls.DerivAPICalls.get_financial_assessment")`
    * `[get_limits](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.get_limits "deriv_api.deriv_api_calls.DerivAPICalls.get_limits")`
    * `[get_self_exclusion](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.get_self_exclusion "deriv_api.deriv_api_calls.DerivAPICalls.get_self_exclusion")`
    * `[get_settings](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.get_settings "deriv_api.deriv_api_calls.DerivAPICalls.get_settings")`
    * `[identity_verification_document_add](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.identity_verification_document_add "deriv_api.deriv_api_calls.DerivAPICalls.identity_verification_document_add")`
    * `[kyc_auth_status](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.kyc_auth_status "deriv_api.deriv_api_calls.DerivAPICalls.kyc_auth_status")`
    * `[landing_company](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.landing_company "deriv_api.deriv_api_calls.DerivAPICalls.landing_company")`
    * `[landing_company_details](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.landing_company_details "deriv_api.deriv_api_calls.DerivAPICalls.landing_company_details")`
    * `[login_history](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.login_history "deriv_api.deriv_api_calls.DerivAPICalls.login_history")`
    * `[logout](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.logout "deriv_api.deriv_api_calls.DerivAPICalls.logout")`
    * `[mt5_deposit](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.mt5_deposit "deriv_api.deriv_api_calls.DerivAPICalls.mt5_deposit")`
    * `[mt5_get_settings](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.mt5_get_settings "deriv_api.deriv_api_calls.DerivAPICalls.mt5_get_settings")`
    * `[mt5_login_list](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.mt5_login_list "deriv_api.deriv_api_calls.DerivAPICalls.mt5_login_list")`
    * `[mt5_new_account](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.mt5_new_account "deriv_api.deriv_api_calls.DerivAPICalls.mt5_new_account")`
    * `[mt5_password_change](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.mt5_password_change "deriv_api.deriv_api_calls.DerivAPICalls.mt5_password_change")`
    * `[mt5_password_check](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.mt5_password_check "deriv_api.deriv_api_calls.DerivAPICalls.mt5_password_check")`
    * `[mt5_password_reset](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.mt5_password_reset "deriv_api.deriv_api_calls.DerivAPICalls.mt5_password_reset")`
    * `[mt5_withdrawal](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.mt5_withdrawal "deriv_api.deriv_api_calls.DerivAPICalls.mt5_withdrawal")`
    * `[new_account_maltainvest](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.new_account_maltainvest "deriv_api.deriv_api_calls.DerivAPICalls.new_account_maltainvest")`
    * `[new_account_real](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.new_account_real "deriv_api.deriv_api_calls.DerivAPICalls.new_account_real")`
    * `[new_account_virtual](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.new_account_virtual "deriv_api.deriv_api_calls.DerivAPICalls.new_account_virtual")`
    * `[oauth_apps](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.oauth_apps "deriv_api.deriv_api_calls.DerivAPICalls.oauth_apps")`
    * `[p2p_advert_create](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advert_create "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advert_create")`
    * `[p2p_advert_info](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advert_info "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advert_info")`
    * `[p2p_advert_list](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advert_list "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advert_list")`
    * `[p2p_advert_update](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advert_update "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advert_update")`
    * `[p2p_advertiser_adverts](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_adverts "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_adverts")`
    * `[p2p_advertiser_create](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_create "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_create")`
    * `[p2p_advertiser_info](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_info "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_info")`
    * `[p2p_advertiser_list](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_list "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_list")`
    * `[p2p_advertiser_payment_methods](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_payment_methods "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_payment_methods")`
    * `[p2p_advertiser_relations](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_relations "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_relations")`
    * `[p2p_advertiser_update](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_update "deriv_api.deriv_api_calls.DerivAPICalls.p2p_advertiser_update")`
    * `[p2p_chat_create](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_chat_create "deriv_api.deriv_api_calls.DerivAPICalls.p2p_chat_create")`
    * `[p2p_order_cancel](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_cancel "deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_cancel")`
    * `[p2p_order_confirm](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_confirm "deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_confirm")`
    * `[p2p_order_create](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_create "deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_create")`
    * `[p2p_order_dispute](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_dispute "deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_dispute")`
    * `[p2p_order_info](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_info "deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_info")`
    * `[p2p_order_list](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_list "deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_list")`
    * `[p2p_order_review](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_review "deriv_api.deriv_api_calls.DerivAPICalls.p2p_order_review")`
    * `[p2p_payment_methods](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_payment_methods "deriv_api.deriv_api_calls.DerivAPICalls.p2p_payment_methods")`
    * `[p2p_ping](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.p2p_ping "deriv_api.deriv_api_calls.DerivAPICalls.p2p_ping")`
    * `[payment_methods](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.payment_methods "deriv_api.deriv_api_calls.DerivAPICalls.payment_methods")`
    * `[paymentagent_create](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_create "deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_create")`
    * `[paymentagent_details](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_details "deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_details")`
    * `[paymentagent_list](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_list "deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_list")`
    * `[paymentagent_transfer](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_transfer "deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_transfer")`
    * `[paymentagent_withdraw](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_withdraw "deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_withdraw")`
    * `[paymentagent_withdraw_justification](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_withdraw_justification "deriv_api.deriv_api_calls.DerivAPICalls.paymentagent_withdraw_justification")`
    * `[payout_currencies](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.payout_currencies "deriv_api.deriv_api_calls.DerivAPICalls.payout_currencies")`
    * `[ping](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.ping "deriv_api.deriv_api_calls.DerivAPICalls.ping")`
    * `[portfolio](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.portfolio "deriv_api.deriv_api_calls.DerivAPICalls.portfolio")`
    * `[profit_table](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.profit_table "deriv_api.deriv_api_calls.DerivAPICalls.profit_table")`
    * `[proposal](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.proposal "deriv_api.deriv_api_calls.DerivAPICalls.proposal")`
    * `[proposal_open_contract](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.proposal_open_contract "deriv_api.deriv_api_calls.DerivAPICalls.proposal_open_contract")`
    * `[reality_check](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.reality_check "deriv_api.deriv_api_calls.DerivAPICalls.reality_check")`
    * `[residence_list](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.residence_list "deriv_api.deriv_api_calls.DerivAPICalls.residence_list")`
    * `[revoke_oauth_app](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.revoke_oauth_app "deriv_api.deriv_api_calls.DerivAPICalls.revoke_oauth_app")`
    * `[sell](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.sell "deriv_api.deriv_api_calls.DerivAPICalls.sell")`
    * `[sell_contract_for_multiple_accounts](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.sell_contract_for_multiple_accounts "deriv_api.deriv_api_calls.DerivAPICalls.sell_contract_for_multiple_accounts")`
    * `[sell_expired](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.sell_expired "deriv_api.deriv_api_calls.DerivAPICalls.sell_expired")`
    * `[set_account_currency](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.set_account_currency "deriv_api.deriv_api_calls.DerivAPICalls.set_account_currency")`
    * `[set_financial_assessment](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.set_financial_assessment "deriv_api.deriv_api_calls.DerivAPICalls.set_financial_assessment")`
    * `[set_self_exclusion](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.set_self_exclusion "deriv_api.deriv_api_calls.DerivAPICalls.set_self_exclusion")`
    * `[set_settings](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.set_settings "deriv_api.deriv_api_calls.DerivAPICalls.set_settings")`
    * `[statement](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.statement "deriv_api.deriv_api_calls.DerivAPICalls.statement")`
    * `[states_list](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.states_list "deriv_api.deriv_api_calls.DerivAPICalls.states_list")`
    * `[ticks](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.ticks "deriv_api.deriv_api_calls.DerivAPICalls.ticks")`
    * `[ticks_history](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.ticks_history "deriv_api.deriv_api_calls.DerivAPICalls.ticks_history")`
    * `[time](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.time "deriv_api.deriv_api_calls.DerivAPICalls.time")`
    * `[tnc_approval](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.tnc_approval "deriv_api.deriv_api_calls.DerivAPICalls.tnc_approval")`
    * `[topup_virtual](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.topup_virtual "deriv_api.deriv_api_calls.DerivAPICalls.topup_virtual")`
    * `[trading_durations](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.trading_durations "deriv_api.deriv_api_calls.DerivAPICalls.trading_durations")`
    * `[trading_platform_investor_password_reset](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.trading_platform_investor_password_reset "deriv_api.deriv_api_calls.DerivAPICalls.trading_platform_investor_password_reset")`
    * `[trading_platform_password_reset](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.trading_platform_password_reset "deriv_api.deriv_api_calls.DerivAPICalls.trading_platform_password_reset")`
    * `[trading_servers](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.trading_servers "deriv_api.deriv_api_calls.DerivAPICalls.trading_servers")`
    * `[trading_times](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.trading_times "deriv_api.deriv_api_calls.DerivAPICalls.trading_times")`
    * `[transaction](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.transaction "deriv_api.deriv_api_calls.DerivAPICalls.transaction")`
    * `[transfer_between_accounts](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.transfer_between_accounts "deriv_api.deriv_api_calls.DerivAPICalls.transfer_between_accounts")`
    * `[unsubscribe_email](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.unsubscribe_email "deriv_api.deriv_api_calls.DerivAPICalls.unsubscribe_email")`
    * `[verify_email](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.verify_email "deriv_api.deriv_api_calls.DerivAPICalls.verify_email")`
    * `[verify_email_cellxpert](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.verify_email_cellxpert "deriv_api.deriv_api_calls.DerivAPICalls.verify_email_cellxpert")`
    * `[website_status](deriv_api_calls.html#deriv_api.deriv_api_calls.DerivAPICalls.website_status "deriv_api.deriv_api_calls.DerivAPICalls.website_status")`

# Index

  * ### Super-module

    * `[deriv_api](index.html "deriv_api")`
  * ### Classes

    * #### `DerivAPI`

      * `subscribe`
      * `forget`
      * `forget_all`
      * `expect_response`
      * `clear`

Generated by [pdoc 0.10.0](https://pdoc3.github.io/pdoc "pdoc: Python API
documentation generator").



---

## Documentation from [https://deriv-com.github.io/python-deriv-api/deriv_api_calls.html](https://deriv-com.github.io/python-deriv-api/deriv_api_calls.html)

# Module `deriv_api.deriv_api_calls`

## Classes

` class DerivAPICalls `

    

### Subclasses

  * [Cache](cache.html#deriv_api.cache.Cache "deriv_api.cache.Cache")
  * [DerivAPI](deriv_api.html#deriv_api.deriv_api.DerivAPI "deriv_api.deriv_api.DerivAPI")

### Methods

` async def active_symbols(self, args=None) `

    

Retrieve a list of all currently active symbols (underlying markets upon which
contracts are available for trading).

## Parameters:

    
    
    args : dict with following keys
        active_symbols : str
            If you use brief, only a subset of fields will be returned.
        landing_company : str
            Deprecated - replaced by landing_company_short.
        landing_company_short : str
            [Optional] If you specify this field, only symbols available for trading by that landing company will be returned. If you are logged in, only symbols available for trading by your landing company will be returned regardless of what you specify in this field.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        product_type : str
            [Optional] If you specify this field, only symbols that can be traded through that product type will be returned.
        req_id : int
            [Optional] Used to map request to response.
    

` async def api_token(self, args=None) `

    

This call manages API tokens

## Parameters:

    
    
    args : dict with following keys
        api_token : int
            Must be 1
        delete_token : str
            [Optional] The token to remove.
        new_token : str
            [Optional] The name of the created token.
        new_token_scopes : Any
            [Optional] List of permission scopes to provide with the token.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        valid_for_current_ip_only : int
            [Optional] If you set this parameter during token creation, then the token created will only work for the IP address that was used to create the token
    

` async def app_delete(self, args=None) `

    

The request for deleting an application.

## Parameters:

    
    
    args : dict with following keys
        app_delete : int
            Application app_id
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def app_get(self, args=None) `

    

To get the information of the OAuth application specified by 'app_id'

## Parameters:

    
    
    args : dict with following keys
        app_get : int
            Application app_id
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def app_list(self, args=None) `

    

List all of the account's OAuth applications

## Parameters:

    
    
    args : dict with following keys
        app_list : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def app_markup_details(self, args=None) `

    

Retrieve details of `app_markup` according to criteria specified.

## Parameters:

    
    
    args : dict with following keys
        app_id : int
            [Optional] Specific application app_id to report on.
        app_markup_details : int
            Must be 1
        client_loginid : str
            [Optional] Specific client loginid to report on, like CR12345
        date_from : str
            Start date (epoch or YYYY-MM-DD HH:MM:SS). Results are inclusive of this time.
        date_to : str
            End date (epoch or YYYY-MM-DD HH::MM::SS). Results are inclusive of this time.
        description : int
            [Optional] If set to 1, will return app_markup transaction details.
        limit : Number
            [Optional] Apply upper limit to count of transactions received.
        offset : int
            [Optional] Number of transactions to skip.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        sort : str
            [Optional] Sort direction on transaction_time. Other fields sort order is ASC.
        sort_fields : Any
            [Optional] One or more of the specified fields to sort on. Default sort field is by transaction_time.
    

` async def app_markup_statistics(self, args=None) `

    

Retrieve statistics of `app_markup`.

## Parameters:

    
    
    args : dict with following keys
        app_markup_statistics : int
            Must be 1
        date_from : str
            Start date (epoch or YYYY-MM-DD HH:MM:SS). Results are inclusive of this time.
        date_to : str
            End date (epoch or YYYY-MM-DD HH::MM::SS). Results are inclusive of this time.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def app_register(self, args=None) `

    

Register a new OAuth application

## Parameters:

    
    
    args : dict with following keys
        app_markup_percentage : Number
            [Optional] Markup to be added to contract prices (as a percentage of contract payout). Max markup: 3%.
        app_register : int
            Must be 1
        appstore : str
            [Optional] Application's App Store URL (if applicable).
        github : str
            [Optional] Application's GitHub page (for open-source projects).
        googleplay : str
            [Optional] Application's Google Play URL (if applicable).
        homepage : str
            [Optional] Application's homepage URL.
        name : str
            Application name.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        redirect_uri : str
            [Optional] The URL to redirect to after a successful login. Required if charging markup percentage
        req_id : int
            [Optional] Used to map request to response.
        scopes : Any
            List of permission scopes to grant the application.
        verification_uri : str
            [Optional] Used when verify_email called. If available, a URL containing the verification token will be sent to the client's email, otherwise only the token will be sent.
    

` async def app_update(self, args=None) `

    

Update a new OAuth application

## Parameters:

    
    
    args : dict with following keys
        app_markup_percentage : Number
            [Optional] Markup to be added to contract prices (as a percentage of contract payout). Max markup: 3%.
        app_update : int
            Application app_id.
        appstore : str
            [Optional] Application's App Store URL (if applicable).
        github : str
            [Optional] Application's GitHub page (for open-source projects).
        googleplay : str
            [Optional] Application's Google Play URL (if applicable).
        homepage : str
            [Optional] Application's homepage URL.
        name : str
            Application name.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        redirect_uri : str
            [Optional] The URL to redirect to after a successful login. Required if charging markup percentage.
        req_id : int
            [Optional] Used to map request to response.
        scopes : Any
            Change scopes will revoke all user's grants and log them out.
        verification_uri : str
            [Optional] Used when verify_email called. If available, a URL containing the verification token will send to the client's email, otherwise only the token will be sent.
    

` async def asset_index(self, args=None) `

    

Retrieve a list of all available underlyings and the corresponding contract
types and duration boundaries. If the user is logged in, only the assets
available for that user's landing company will be returned.

## Parameters:

    
    
    args : dict with following keys
        asset_index : int
            Must be 1
        landing_company : str
            Deprecated - replaced by landing_company_short.
        landing_company_short : str
            [Optional] If specified, will return only the underlyings for the specified landing company.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def authorize(self, args=None) `

    

Authorize current WebSocket session to act on behalf of the owner of a given
token. Must precede requests that need to access client account, for example
purchasing and selling contracts or viewing portfolio.

## Parameters:

    
    
    args : dict with following keys
        add_to_login_history : int
            [Optional] Send this when you use api tokens for authorization and want to track activity using login_history call.
        authorize : str
            Authentication token. May be retrieved from <https://www.binary.com/en/user/security/api_tokenws.html>
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def balance(self, args=None) `

    

Get user account balance

## Parameters:

    
    
    args : dict with following keys
        account : str
            [Optional] If set to all, return the balances of all accounts one by one; if set to current, return the balance of current account; if set as an account id, return the balance of that account.
        balance : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        subscribe : int
            [Optional] If set to 1, will send updates whenever the balance changes.
    

` async def buy(self, args=None) `

    

Buy a Contract

## Parameters:

    
    
    args : dict with following keys
        buy : str
            Either the ID received from a Price Proposal (proposal call), or 1 if contract buy parameters are passed in the parameters field.
        parameters : Any
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        price : Number
            Maximum price at which to purchase the contract.
        req_id : int
            [Optional] Used to map request to response.
        subscribe : int
            [Optional] 1 to stream.
    

` async def buy_contract_for_multiple_accounts(self, args=None) `

    

Buy a Contract for multiple Accounts specified by the `tokens` parameter.
Note, although this is an authorized call, the contract is not bought for the
authorized account.

## Parameters:

    
    
    args : dict with following keys
        buy_contract_for_multiple_accounts : str
            Either the ID received from a Price Proposal (proposal call), or 1 if contract buy parameters are passed in the parameters field.
        parameters : Any
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        price : Number
            Maximum price at which to purchase the contract.
        req_id : int
            [Optional] Used to map request to response.
        tokens : Any
            List of API tokens identifying the accounts for which the contract is bought. Note: If the same token appears multiple times or if multiple tokens designate the same account, the contract is bought multiple times for this account.
    

` async def cancel(self, args=None) `

    

Cancel contract with contract id

## Parameters:

    
    
    args : dict with following keys
        cancel : int
            Value should be the contract_id which received from the portfolio call.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def cashier(self, args=None) `

    

Request the cashier info for the specified type.

## Parameters:

    
    
    args : dict with following keys
        address : str
            [Optional] Address for crypto withdrawal. Only applicable for api type.
        amount : Number
            [Optional] Amount for crypto withdrawal. Only applicable for api type.
        cashier : str
            Operation which needs to be requested from cashier
        dry_run : int
            [Optional] If set to 1, only validation is performed. Only applicable for withdraw using crypto provider and api type.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        provider : str
            [Optional] Cashier provider. crypto will be default option for crypto currency accounts.
        req_id : int
            [Optional] Used to map request to response.
        type : str
            [Optional] Data need to be returned from cashier. api is supported only for crypto provider.
        verification_code : str
            [Optional] Email verification code (received from a verify_email call, which must be done first)
    

` async def contract_update(self, args=None) `

    

Update a contract condition.

## Parameters:

    
    
    args : dict with following keys
        contract_id : int
            Internal unique contract identifier.
        contract_update : int
            Must be 1
        limit_order : Any
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def contract_update_history(self, args=None) `

    

Request for contract update history.

## Parameters:

    
    
    args : dict with following keys
        contract_id : int
            Internal unique contract identifier.
        contract_update_history : int
            Must be 1
        limit : Number
            [Optional] Maximum number of historical updates to receive.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def contracts_for(self, args=None) `

    

For a given symbol, get the list of currently available contracts, and the
latest barrier and duration limits for each contract.

## Parameters:

    
    
    args : dict with following keys
        contracts_for : str
            The short symbol name (obtained from active_symbols call).
        currency : str
            [Optional] Currency of the contract's stake and payout (obtained from payout_currencies call).
        landing_company : str
            Deprecated - Replaced by landing_company_short.
        landing_company_short : str
            [Optional] Indicates which landing company to get a list of contracts for. If you are logged in, your account's landing company will override this field. Note that when landing_company_short is set to 'virtual', landing_company will take precendce until the deprecated field is removed from the api.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        product_type : str
            [Optional] If you specify this field, only contracts tradable through that contract type will be returned.
        req_id : int
            [Optional] Used to map request to response.
    

` async def copy_start(self, args=None) `

    

Start copy trader bets

## Parameters:

    
    
    args : dict with following keys
        assets : Any
            [Optional] Used to set assets to be copied. E.x ["frxUSDJPY", "R_50"]
        copy_start : str
            API tokens identifying the accounts of trader which will be used to copy trades
        max_trade_stake : Number
            [Optional] Used to set maximum trade stake to be copied.
        min_trade_stake : Number
            [Optional] Used to set minimal trade stake to be copied.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        trade_types : Any
            [Optional] Used to set trade types to be copied. E.x ["CALL", "PUT"]
    

` async def copy_stop(self, args=None) `

    

Stop copy trader bets

## Parameters:

    
    
    args : dict with following keys
        copy_stop : str
            API tokens identifying the accounts which needs not to be copied
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def copytrading_list(self, args=None) `

    

Retrieves a list of active copiers and/or traders for Copy Trading

## Parameters:

    
    
    args : dict with following keys
        copytrading_list : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def copytrading_statistics(self, args=None) `

    

Retrieve performance, trading, risk and copiers statistics of trader.

## Parameters:

    
    
    args : dict with following keys
        copytrading_statistics : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        trader_id : str
            The ID of the target trader.
    

` async def crypto_config(self, args=None) `

    

The request for cryptocurrencies configuration.

## Parameters:

    
    
    args : dict with following keys
        crypto_config : int
            Must be 1
        currency_code : str
            [Optional] Cryptocurrency code. Sending request with currency_code provides crypto config for the sent cryptocurrency code only.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def document_upload(self, args=None) `

    

Request KYC information from client

## Parameters:

    
    
    args : dict with following keys
        document_format : str
            Document file format
        document_id : str
            [Optional] Document ID (required for Passport, Proof of ID and Driver's License)
        document_issuing_country : str
            2-letter country code, mandatory for POI only
        document_type : str
            Document type
        document_upload : int
            Must be 1
        expected_checksum : str
            The checksum of the file to be uploaded
        expiration_date : str
            [Optional] Document expiration date (required for Passport, Proof of ID and Driver's License)
        file_size : int
            Document size (should be less than 10MB)
        lifetime_valid : int
            [Optional] Boolean value that indicates whether this document is lifetime valid (only applies to POI document types, cancels out the expiration_date given if any)
        page_type : str
            [Optional] To determine document side
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        proof_of_ownership : Any
        req_id : int
            [Optional] Used to map request to response.
    

` async def economic_calendar(self, args=None) `

    

Specify a currency to receive a list of events related to that specific
currency. For example, specifying USD will return a list of USD-related
events. If the currency is omitted, you will receive a list for all
currencies.

## Parameters:

    
    
    args : dict with following keys
        currency : str
            [Optional] Currency symbol.
        economic_calendar : int
            Must be 1
        end_date : int
            [Optional] End date.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        start_date : int
            [Optional] Start date.
    

` async def exchange_rates(self, args=None) `

    

Retrieves the exchange rates from a base currency to all currencies supported
by the system.

## Parameters:

    
    
    args : dict with following keys
        base_currency : str
            Base currency (can be obtained from payout_currencies call)
        exchange_rates : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        subscribe : int
            [Optional] 1 - to initiate a realtime stream of exchange rates relative to base currency.
        target_currency : str
            [Optional] Local currency
    

` async def forget(self, args=None) `

    

Immediately cancel the real-time stream of messages with a specific ID.

## Parameters:

    
    
    args : dict with following keys
        forget : str
            ID of the real-time stream of messages to cancel.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def forget_all(self, args=None) `

    

Immediately cancel the real-time streams of messages of given type.

## Parameters:

    
    
    args : dict with following keys
        forget_all : Any
            Cancel all streams by type. The value can be either a single type e.g. "ticks", or an array of multiple types e.g. ["candles", "ticks"].
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def get_account_status(self, args=None) `

    

Get Account Status

## Parameters:

    
    
    args : dict with following keys
        get_account_status : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def get_financial_assessment(self, args=None) `

    

This call gets the financial assessment details. The 'financial assessment' is
a questionnaire that clients of certain Landing Companies need to complete,
due to regulatory and KYC (know your client) requirements.

## Parameters:

    
    
    args : dict with following keys
        get_financial_assessment : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def get_limits(self, args=None) `

    

Trading and Withdrawal Limits for a given user

## Parameters:

    
    
    args : dict with following keys
        get_limits : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def get_self_exclusion(self, args=None) `

    

Allows users to exclude themselves from the website for certain periods of
time, or to set limits on their trading activities. This facility is a
regulatory requirement for certain Landing Companies.

## Parameters:

    
    
    args : dict with following keys
        get_self_exclusion : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def get_settings(self, args=None) `

    

Get User Settings (email, date of birth, address etc)

## Parameters:

    
    
    args : dict with following keys
        get_settings : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def identity_verification_document_add(self, args=None) `

    

Adds document information such as issuing country, id and type for identity
verification processes.

## Parameters:

    
    
    args : dict with following keys
        document_additional : str
            [Optional] Additional info required by some document types.
        document_number : str
            The identification number of the document.
        document_type : str
            The type of the document based on provided issuing_country (can obtained from residence_list call).
        identity_verification_document_add : int
            Must be 1
        issuing_country : str
            2-letter country code (can obtained from residence_list call).
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def kyc_auth_status(self, args=None) `

    

Get KYC Authentication Status

## Parameters:

    
    
    args : dict with following keys
        kyc_auth_status : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def landing_company(self, args=None) `

    

The company has a number of licensed subsidiaries in various jurisdictions,
which are called Landing Companies. This call will return the appropriate
Landing Company for clients of a given country. The landing company may differ
for Gaming contracts (Synthetic Indices) and Financial contracts (Forex, Stock
Indices, Commodities).

## Parameters:

    
    
    args : dict with following keys
        landing_company : str
            Client's 2-letter country code (obtained from residence_list call).
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def landing_company_details(self, args=None) `

    

The company has a number of licensed subsidiaries in various jurisdictions,
which are called Landing Companies (and which are wholly owned subsidiaries of
the Deriv Group). This call provides information about each Landing Company.

## Parameters:

    
    
    args : dict with following keys
        country : str
            [Optional] Will return an extra field tin_not_mandatory indicating if the landing company does not require tax identification number for the provided country.
        landing_company_details : str
            Landing company shortcode.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def login_history(self, args=None) `

    

Retrieve a summary of login history for user.

## Parameters:

    
    
    args : dict with following keys
        limit : int
            [Optional] Apply limit to count of login history records.
        login_history : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def logout(self, args=None) `

    

Logout the session

## Parameters:

    
    
    args : dict with following keys
        logout : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def mt5_deposit(self, args=None) `

    

This call allows deposit into MT5 account from Binary account.

## Parameters:

    
    
    args : dict with following keys
        amount : Number
            Amount to deposit (in the currency of from_binary); min = $1 or an equivalent amount, max = $20000 or an equivalent amount
        from_binary : str
            Binary account loginid to transfer money from
        mt5_deposit : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        to_mt5 : str
            MT5 account login to deposit money to
    

` async def mt5_get_settings(self, args=None) `

    

Get MT5 user account settings

## Parameters:

    
    
    args : dict with following keys
        login : str
            MT5 user login
        mt5_get_settings : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def mt5_login_list(self, args=None) `

    

Get list of MT5 accounts for client

## Parameters:

    
    
    args : dict with following keys
        mt5_login_list : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def mt5_new_account(self, args=None) `

    

This call creates new MT5 user, either demo or real money user.

## Parameters:

    
    
    args : dict with following keys
        account_type : str
            Account type. If set to 'financial', setting 'mt5_account_type' is also required.
        address : str
            [Optional] The address of the user. The maximum length of this address field is 128 characters.
        city : str
            [Optional] User's city of residence.
        company : str
            [Optional] Name of the client's company. The maximum length of the company name is 64 characters.
        country : str
            [Optional] 2-letter country code (value received from residence_list call).
        currency : str
            [Optional] MT5 account currency, the default value will be the qualified account currency.
        dry_run : int
            [Optional] If set to 1, only validation is performed.
        email : str
            Email address
        investPassword : str
            [Optional] The investor password of the account. For validation (Accepts any printable ASCII character. Must be within 8-25 characters, and include numbers, lowercase and uppercase letters. Must not be the same as the user's email address).
        leverage : Number
            Client leverage (from 1 to 1000).
        mainPassword : str
            The master password of the account. For validation (Accepts any printable ASCII character. Must be within 8-25 characters, and include numbers, lowercase and uppercase letters. Must not be the same as the user's email address). This field is required.
        mt5_account_category : str
            [Optional] To choose whether account is conventional or swap_free. Unavailable for financial_stp MT5_account_type
        mt5_account_type : str
            [Optional] Financial: Variable spreads, High leverage. Financial STP: Variable spreads, Medium Leverage, more products. If 'account_type' set to 'financial', setting 'mt5_account_type' is also required.
        mt5_new_account : int
            Must be 1
        name : str
            Client's name. The maximum length here is 101 characters.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        phone : Any
            [Optional] User's phone number.
        phonePassword : str
            [Optional] The user's phone password.
        req_id : int
            [Optional] Used to map request to response.
        server : Any
            [Optional] Trade server.
        state : str
            [Optional] User's state (region) of residence.
        sub_account_category : str
            [Optional] Indicate the sub account category that we have in the cfd group naming convention.
        zipCode : str
            [Optional] User's zip code.
    

` async def mt5_password_change(self, args=None) `

    

To change passwords of the MT5 account.

## Parameters:

    
    
    args : dict with following keys
        login : str
            MT5 user login
        mt5_password_change : int
            Must be 1
        new_password : str
            New password of the account. For validation (Accepts any printable ASCII character. Must be within 8-25 characters, and include numbers, lowercase and uppercase letters. Must not be the same as the user's email address).
        old_password : str
            Old password for validation (non-empty string, accepts any printable ASCII character)
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        password_type : str
            [Optional] Type of the password to change.
        req_id : int
            [Optional] Used to map request to response.
    

` async def mt5_password_check(self, args=None) `

    

This call validates the main password for the MT5 user

## Parameters:

    
    
    args : dict with following keys
        login : str
            MT5 user login
        mt5_password_check : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        password : str
            The password of the account.
        password_type : str
            [Optional] Type of the password to check.
        req_id : int
            [Optional] Used to map request to response.
    

` async def mt5_password_reset(self, args=None) `

    

To reset the password of MT5 account.

## Parameters:

    
    
    args : dict with following keys
        login : str
            MT5 user login
        mt5_password_reset : int
            Must be 1
        new_password : str
            New password of the account. For validation (Accepts any printable ASCII character. Must be within 8-25 characters, and include numbers, lowercase and uppercase letters. Must not be the same as the user's email address).
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        password_type : str
            [Optional] Type of the password to reset.
        req_id : int
            [Optional] Used to map request to response.
        verification_code : str
            Email verification code (received from a verify_email call, which must be done first)
    

` async def mt5_withdrawal(self, args=None) `

    

This call allows withdrawal from MT5 account to Binary account.

## Parameters:

    
    
    args : dict with following keys
        amount : Number
            Amount to withdraw (in the currency of the MT5 account); min = $1 or an equivalent amount, max = $20000 or an equivalent amount.
        from_mt5 : str
            MT5 account login to withdraw money from
        mt5_withdrawal : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        to_binary : str
            Binary account loginid to transfer money to
    

` async def new_account_maltainvest(self, args=None) `

    

This call opens a new real-money account with the `maltainvest` Landing
Company. This call can be made from a virtual-money account or real-money
account at Deriv (Europe) Limited. If it is the latter, client information
fields in this call will be ignored and data from your existing real-money
account will be used.

## Parameters:

    
    
    args : dict with following keys
        accept_risk : int
            Show whether client has accepted risk disclaimer.
        account_opening_reason : str
            [Optional] Purpose and reason for requesting the account opening.
        account_turnover : str
            [Optional] The anticipated account turnover.
        address_city : str
            Within 100 characters
        address_line_1 : str
            Within 70 characters, with no leading whitespaces and may contain letters/numbers and/or any of following characters '.,:;()@#/-
        address_line_2 : str
            [Optional] Within 70 characters.
        address_postcode : str
            [Optional] Within 20 characters and may not contain '+'.
        address_state : str
            [Optional] Possible value receive from states_list call.
        affiliate_token : str
            [Optional] Affiliate token, within 32 characters.
        cfd_experience : str
            How much experience do you have in CFD trading?
        cfd_frequency : str
            How many CFD trades have you placed in the past 12 months?
        cfd_trading_definition : str
            In your understanding, CFD trading allows you to:
        citizen : str
            [Optional] Country of legal citizenship, 2-letter country code. Possible value receive from residence_list call.
        client_type : str
            [Optional] Indicates whether this is for a client requesting an account with professional status.
        currency : str
            [Optional] To set currency of the account. List of supported currencies can be acquired with payout_currencies call.
        date_of_birth : str
            Date of birth format: yyyy-mm-dd.
        education_level : str
            Level of Education
        employment_industry : str
            Industry of Employment.
        employment_status : str
            Employment Status.
        estimated_worth : str
            Estimated Net Worth.
        first_name : str
            Within 2-50 characters, use only letters, spaces, hyphens, full-stops or apostrophes.
        income_source : str
            Income Source.
        last_name : str
            Within 2-50 characters, use only letters, spaces, hyphens, full-stops or apostrophes.
        leverage_impact_trading : str
            How does leverage affect CFD trading?
        leverage_trading_high_risk_stop_loss : str
            Leverage trading is high-risk, so it's a good idea to use risk management features such as stop loss. Stop loss allows you to
        net_income : str
            Net Annual Income.
        new_account_maltainvest : int
            Must be 1
        non_pep_declaration : int
            [Optional] Indicates client's self-declaration of not being a PEP/RCA.
        occupation : str
            Occupation.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        phone : Any
            [Optional] Starting with + followed by 9-35 digits, hyphens or space.
        place_of_birth : str
            [Optional] Place of birth, 2-letter country code.
        req_id : int
            [Optional] Used to map request to response.
        required_initial_margin : str
            When would you be required to pay an initial margin?
        residence : str
            2-letter country code, possible value receive from residence_list call.
        risk_tolerance : str
            Do you understand that you could potentially lose 100% of the money you use to trade?
        salutation : str
            Accept any value in enum list.
        secret_answer : str
            [Optional] Answer to secret question, within 4-50 characters.
        secret_question : str
            [Optional] Accept any value in enum list.
        source_of_experience : str
            How much knowledge and experience do you have in relation to online trading?
        source_of_wealth : str
            [Optional] Source of wealth.
        tax_identification_number : str
            Tax identification number. Only applicable for real money account. Required for maltainvest landing company.
        tax_residence : str
            Residence for tax purpose. Comma separated iso country code if multiple jurisdictions. Only applicable for real money account. Required for maltainvest landing company.
        trading_experience_financial_instruments : str
            How much experience do you have with other financial instruments?
        trading_frequency_financial_instruments : str
            How many trades have you placed with other financial instruments in the past 12 months?
    

` async def new_account_real(self, args=None) `

    

This call opens a new real-money account. This call can be made from a
virtual-money or a real-money account. If it is the latter, client information
fields in this call will be ignored and data from your existing real-money
account will be used.

## Parameters:

    
    
    args : dict with following keys
        account_opening_reason : str
            [Optional] Purpose and reason for requesting the account opening.
        account_turnover : str
            [Optional] The anticipated account turnover.
        address_city : str
            [Optional] Within 100 characters.
        address_line_1 : str
            Within 70 characters, with no leading whitespaces and may contain letters/numbers and/or any of following characters '.,:;()@#/-
        address_line_2 : str
            [Optional] Within 70 characters.
        address_postcode : str
            [Optional] Within 20 characters and may not contain '+'.
        address_state : str
            [Optional] Possible value receive from states_list call.
        affiliate_token : str
            [Optional] Affiliate token, within 32 characters.
        citizen : Any
            [Optional] Country of legal citizenship, 2-letter country code.
        client_type : str
            [Optional] Indicates whether this is for a client requesting an account with professional status.
        currency : str
            [Optional] To set currency of the account. List of supported currencies can be acquired with payout_currencies call.
        date_of_birth : str
            Date of birth format: yyyy-mm-dd.
        first_name : str
            Within 2-50 characters, use only letters, spaces, hyphens, full-stops or apostrophes.
        last_name : str
            Within 2-50 characters, use only letters, spaces, hyphens, full-stops or apostrophes.
        new_account_real : int
            Must be 1
        non_pep_declaration : int
            [Optional] Indicates client's self-declaration of not being a PEP/RCA (Politically Exposed Person/Relatives and Close Associates).
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        phone : Any
            [Optional] Starting with + followed by 9-35 digits, hyphens or space.
        place_of_birth : str
            [Optional] Place of birth, 2-letter country code.
        req_id : int
            [Optional] Used to map request to response.
        residence : str
            2-letter country code, possible value receive from residence_list call.
        salutation : str
            [Optional] Accept any value in enum list.
        secret_answer : str
            [Optional] Answer to secret question, within 4-50 characters. Required for new account and existing client details will be used if client open another account.
        secret_question : str
            [Optional] Accept any value in enum list. Required for new account and existing client details will be used if client open another account.
        tax_identification_number : str
            [Optional] Tax identification number. Only applicable for real money account. Required for maltainvest landing company.
        tax_residence : str
            [Optional] Residence for tax purpose. Comma separated iso country code if multiple jurisdictions. Only applicable for real money account. Required for maltainvest landing company.
    

` async def new_account_virtual(self, args=None) `

    

Create a new virtual-money account.

## Parameters:

    
    
    args : dict with following keys
        affiliate_token : str
            [Optional] Affiliate token, within 32 characters.
        client_password : str
            Password (Accepts any printable ASCII character. Must be within 8-25 characters, and include numbers, lowercase and uppercase letters. Must not be the same as the user's email address).
        date_first_contact : str
            [Optional] Date of first contact, format: yyyy-mm-dd in GMT timezone.
        email_consent : int
            [Optional] Boolean value: 1 or 0, indicating whether the client has given consent for marketing emails.
        gclid_url : str
            [Optional] Google Click Identifier to track source.
        new_account_virtual : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        residence : str
            2-letter country code (obtained from residence_list call).
        signup_device : str
            [Optional] Show whether user has used mobile or desktop.
        type : str
            Account type
        utm_ad_id : Any
            [Optional] Identifier of particular ad. Value must match Regex pattern to be recorded
        utm_adgroup_id : Any
            [Optional] Identifier of ad group in the campaign. Value must match Regex pattern to be recorded
        utm_adrollclk_id : Any
            [Optional] Unique identifier of click on AdRoll ads platform. Value must match Regex pattern to be recorded
        utm_campaign : Any
            [Optional] Identifies a specific product promotion or strategic campaign such as a spring sale or other promotions. Value must match Regex pattern to be recorded
        utm_campaign_id : Any
            [Optional] Identifier of paid ad campaign. Value must match Regex pattern to be recorded
        utm_content : Any
            [Optional] Used to differentiate similar content, or links within the same ad. Value must match Regex pattern to be recorded
        utm_fbcl_id : Any
            [Optional] Unique identifier of click on Facebook ads platform. Value must match Regex pattern to be recorded
        utm_gl_client_id : Any
            [Optional] Unique visitor identifier on Google Ads platform. Value must match Regex pattern to be recorded
        utm_medium : Any
            [Optional] Identifies the medium the link was used upon such as: email, CPC, or other methods of sharing. Value must match Regex pattern to be recorded
        utm_msclk_id : Any
            [Optional] Unique click identifier on Microsoft Bing ads platform. Value must match Regex pattern to be recorded
        utm_source : Any
            [Optional] Identifies the source of traffic such as: search engine, newsletter, or other referral. Value must match Regex pattern to be recorded
        utm_term : Any
            [Optional] Used to send information related to the campaign term like paid search keywords. Value must match Regex pattern to be recorded
        verification_code : str
            Email verification code (received from a verify_email call, which must be done first).
    

` async def oauth_apps(self, args=None) `

    

List all my used OAuth applications.

## Parameters:

    
    
    args : dict with following keys
        oauth_apps : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def p2p_advert_create(self, args=None) `

    

Creates a P2P (Peer to Peer) advert. Can only be used by an approved P2P
advertiser.

## Parameters:

    
    
    args : dict with following keys
        amount : Number
            The total amount of the advert, in advertiser's account currency.
        block_trade : int
            [Optional] Indicates if this is block trade ad or not. Default: 0.
        contact_info : str
            [Optional] Advertiser contact information.
        description : str
            [Optional] General information about the advert.
        local_currency : str
            [Optional] Local currency for this advert. If not provided, will use the currency of client's residence by default.
        max_order_amount : Number
            Maximum allowed amount for the orders of this advert, in advertiser's account_currency. Should be more than or equal to min_order_amount
        min_order_amount : Number
            Minimum allowed amount for the orders of this advert, in advertiser's account_currency. Should be less than or equal to max_order_amount.
        p2p_advert_create : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        payment_info : str
            [Optional] Payment instructions.
        payment_method : str
            [Optional] Payment method name (deprecated).
        payment_method_ids : Any
            IDs of previously saved payment methods as returned from p2p_advertiser_payment_methods, only applicable for sell ads.
        payment_method_names : Any
            Payment method identifiers as returned from p2p_payment_methods, only applicable for buy ads.
        rate : Number
            Conversion rate from advertiser's account currency to local_currency. An absolute rate value (fixed), or percentage offset from current market rate (floating).
        rate_type : str
            Type of rate, fixed or floating.
        req_id : int
            [Optional] Used to map request to response.
        type : str
            The advertisement represents the intention to perform this action on your Deriv account funds.
    

` async def p2p_advert_info(self, args=None) `

    

Retrieve information about a P2P advert.

## Parameters:

    
    
    args : dict with following keys
        id : str
            [Optional] The unique identifier for this advert. Optional when subscribe is 1. If not provided, all advertiser adverts will be subscribed.
        p2p_advert_info : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        subscribe : int
            [Optional] If set to 1, will send updates when changes occur. Optional when id is provided.
        use_client_limits : int
            [Optional] If set to 1, the maximum order amount will be adjusted to the current balance and turnover limits of the account.
    

` async def p2p_advert_list(self, args=None) `

    

Returns available adverts for use with `p2p_order_create` .

## Parameters:

    
    
    args : dict with following keys
        advertiser_id : str
            [Optional] ID of the advertiser to list adverts for.
        advertiser_name : str
            [Optional] Search for advertiser by name. Partial matches will be returned.
        amount : Number
            [Optional] How much to buy or sell, used to calculate prices.
        block_trade : int
            [Optional] Return block trade adverts when 1, non-block trade adverts when 0 (default).
        counterparty_type : str
            [Optional] Filter the adverts by counterparty_type.
        favourites_only : int
            [Optional] Only show adverts from favourite advertisers. Default is 0.
        limit : int
            [Optional] Used for paging.
        local_currency : str
            [Optional] Currency to conduct payment transaction in. If not provided, only ads from country of residence will be returned.
        offset : int
            [Optional] Used for paging.
        p2p_advert_list : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        payment_method : Any
            [Optional] Search by supported payment methods.
        req_id : int
            [Optional] Used to map request to response.
        sort_by : str
            [Optional] How the results are sorted.
        use_client_limits : int
            [Optional] If set to 1, ads that exceed this account's balance or turnover limits will not be shown.
    

` async def p2p_advert_update(self, args=None) `

    

Updates a P2P advert. Can only be used by the advertiser.

## Parameters:

    
    
    args : dict with following keys
        contact_info : str
            [Optional] Advertiser contact information.
        delete : int
            [Optional] If set to 1, permanently deletes the advert.
        description : str
            [Optional] General information about the advert.
        id : str
            The unique identifier for this advert.
        is_active : int
            [Optional] Activate or deactivate the advert.
        local_currency : str
            [Optional] Local currency for this advert.
        max_order_amount : Number
            [Optional] Maximum allowed amount for the orders of this advert, in advertiser's account_currency. Should be more than or equal to min_order_amount.
        min_order_amount : Number
            [Optional] Minimum allowed amount for the orders of this advert, in advertiser's account_currency. Should be less than or equal to max_order_amount.
        p2p_advert_update : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        payment_info : str
            [Optional] Payment instructions.
        payment_method_ids : Any
            [Optional] IDs of previously saved payment methods as returned from p2p_advertiser_payment_methods, only applicable for sell ads. Exisiting methods will be replaced.
        payment_method_names : Any
            [Optional] Payment method identifiers as returned from p2p_payment_methods, only applicable for buy ads. Exisiting methods will be replaced.
        rate : Number
            [Optional] Conversion rate from advertiser's account currency to local_currency. An absolute rate value (fixed), or percentage offset from current market rate (floating).
        rate_type : str
            [Optional] Type of rate, fixed or floating.
        remaining_amount : Number
            [Optional] The total available amount of the advert, in advertiser's account currency.
        req_id : int
            [Optional] Used to map request to response.
    

` async def p2p_advertiser_adverts(self, args=None) `

    

Returns all P2P adverts created by the authorized client. Can only be used by
a registered P2P advertiser.

## Parameters:

    
    
    args : dict with following keys
        limit : int
            [Optional] Used for paging. This value will also apply to subsription responses.
        offset : int
            [Optional] Used for paging. This value will also apply to subsription responses.
        p2p_advertiser_adverts : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def p2p_advertiser_create(self, args=None) `

    

Registers the client as a P2P advertiser.

## Parameters:

    
    
    args : dict with following keys
        contact_info : str
            [Optional] Advertiser's contact information, to be used as a default for new sell adverts.
        default_advert_description : str
            [Optional] Default description that can be used every time an advert is created.
        name : str
            The advertiser's displayed name.
        p2p_advertiser_create : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        payment_info : str
            [Optional] Advertiser's payment information, to be used as a default for new sell adverts.
        req_id : int
            [Optional] Used to map request to response.
        subscribe : int
            [Optional] If set to 1, will send updates whenever there is an update to advertiser
    

` async def p2p_advertiser_info(self, args=None) `

    

Retrieve information about a P2P advertiser.

## Parameters:

    
    
    args : dict with following keys
        id : str
            [Optional] The unique identifier for this advertiser. If not provided, returns advertiser information about the current account.
        p2p_advertiser_info : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        subscribe : int
            [Optional] If set to 1, will send updates whenever there is an update to advertiser
    

` async def p2p_advertiser_list(self, args=None) `

    

Retrieve advertisers has/had trade with the current advertiser.

## Parameters:

    
    
    args : dict with following keys
        advertiser_name : str
            [Optional] Search for advertiser by name. Partial matches will be returned.
        is_blocked : int
            [Optional] Used to return only blocked or unblocked partners
        limit : int
            [Optional] Used for paging.
        offset : int
            [Optional] Used for paging.
        p2p_advertiser_list : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        sort_by : str
            [Optional] How the results are sorted.
        trade_partners : int
            [Optional] Get all advertisers has/had trade.
    

` async def p2p_advertiser_payment_methods(self, args=None) `

    

Manage or list P2P advertiser payment methods.

## Parameters:

    
    
    args : dict with following keys
        create : Any
            Contains new payment method entries.
        delete : Any
            Contains payment methods to delete.
        p2p_advertiser_payment_methods : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        update : Any
            Contains payment methods to update.
    

` async def p2p_advertiser_relations(self, args=None) `

    

Updates and returns favourite and blocked advertisers of the current user.

## Parameters:

    
    
    args : dict with following keys
        add_blocked : Any
            IDs of advertisers to block.
        add_favourites : Any
            IDs of advertisers to add as favourites.
        p2p_advertiser_relations : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        remove_blocked : Any
            IDs of advertisers to remove from blocked.
        remove_favourites : Any
            IDs of advertisers to remove from favourites.
        req_id : int
            [Optional] Used to map request to response.
    

` async def p2p_advertiser_update(self, args=None) `

    

Update the information of the P2P advertiser for the current account. Can only
be used by an approved P2P advertiser.

## Parameters:

    
    
    args : dict with following keys
        contact_info : str
            [Optional] Advertiser's contact information, to be used as a default for new sell adverts.
        default_advert_description : str
            [Optional] Default description that can be used every time an advert is created.
        is_listed : int
            [Optional] Used to set if the advertiser's adverts could be listed. When 0, adverts won't be listed regardless of they are active or not. This doesn't change the is_active of each individual advert.
        p2p_advertiser_update : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        payment_info : str
            [Optional] Advertiser's payment information, to be used as a default for new sell adverts.
        req_id : int
            [Optional] Used to map request to response.
        show_name : int
            [Optional] When 1, the advertiser's real name will be displayed on to other users on adverts and orders.
        upgrade_limits : int
            [Optional] Used to upgrade daily limits of eligible advertiser.
    

` async def p2p_chat_create(self, args=None) `

    

Creates a P2P chat for the specified order.

## Parameters:

    
    
    args : dict with following keys
        order_id : str
            The unique identifier for the order to create the chat for.
        p2p_chat_create : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def p2p_order_cancel(self, args=None) `

    

Cancel a P2P order.

## Parameters:

    
    
    args : dict with following keys
        id : str
            The unique identifier for this order.
        p2p_order_cancel : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def p2p_order_confirm(self, args=None) `

    

Confirm a P2P order.

## Parameters:

    
    
    args : dict with following keys
        dry_run : int
            [Optional] If set to 1, only validation is performed.
        id : str
            The unique identifier for this order.
        p2p_order_confirm : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        verification_code : str
            [Optional] Verification code received from email.
    

` async def p2p_order_create(self, args=None) `

    

Creates a P2P order for the specified advert.

## Parameters:

    
    
    args : dict with following keys
        advert_id : str
            The unique identifier for the advert to create an order against.
        amount : Number
            The amount of currency to be bought or sold.
        contact_info : str
            [Optional] Seller contact information. Only applicable for 'sell orders'.
        p2p_order_create : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        payment_info : str
            [Optional] Payment instructions, only applicable for sell orders.
        payment_method_ids : Any
            IDs of payment methods, only applicable for sell orders.
        rate : Number
            [Optional] Conversion rate from account currency to local currency, only applicable for floating rate adverts.
        req_id : int
            [Optional] Used to map request to response.
        subscribe : int
            [Optional] If set to 1, will send updates whenever there is an update to the order.
    

` async def p2p_order_dispute(self, args=None) `

    

Dispute a P2P order.

## Parameters:

    
    
    args : dict with following keys
        dispute_reason : str
            The predefined dispute reason
        id : str
            The unique identifier for this order.
        p2p_order_dispute : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def p2p_order_info(self, args=None) `

    

Retrieves the information about a P2P order.

## Parameters:

    
    
    args : dict with following keys
        id : str
            The unique identifier for the order.
        p2p_order_info : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        subscribe : int
            [Optional] If set to 1, will send updates whenever there is an update to order
    

` async def p2p_order_list(self, args=None) `

    

List active orders.

## Parameters:

    
    
    args : dict with following keys
        active : Number
            [Optional] Should be 1 to list active, 0 to list inactive (historical).
        advert_id : str
            [Optional] If present, lists orders applying to a specific advert.
        date_from : str
            [Optional] Filter the orders created after this date(included) format(epoch or YYYY-MM-DD)
        date_to : str
            [Optional] Filter the orders created before this date(included) format(epoch or YYYY-MM-DD)
        limit : int
            [Optional] Used for paging.
        offset : int
            [Optional] Used for paging.
        p2p_order_list : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        subscribe : int
            [Optional] If set to 1, will send updates whenever there is a change to any order belonging to you.
    

` async def p2p_order_review(self, args=None) `

    

Creates a review for the specified order.

## Parameters:

    
    
    args : dict with following keys
        order_id : str
            The order identification number.
        p2p_order_review : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        rating : int
            Rating for the transaction, 1 to 5.
        recommended : Any
            [Optional] 1 if the counterparty is recommendable to others, otherwise 0.
        req_id : int
            [Optional] Used to map request to response.
    

` async def p2p_payment_methods(self, args=None) `

    

List all P2P payment methods.

## Parameters:

    
    
    args : dict with following keys
        p2p_payment_methods : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def p2p_ping(self, args=None) `

    

Keeps the connection alive and updates the P2P advertiser's online status. The
advertiser will be considered offline 60 seconds after a call is made.

## Parameters:

    
    
    args : dict with following keys
        p2p_ping : int
            Must be 1
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
    

` async def payment_methods(self, args=None) `

    

Will return a list payment methods available for the given country. If the
request is authenticated the client's residence country will be used.

## Parameters:

    
    
    args : dict with following keys
        country : str
            [Optional] 2-letter country code (ISO standard).
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        payment_methods : int
            Must be 1
        req_id : int
            [Optional] Used to map request to response.
    

` async def paymentagent_create(self, args=None) `

    

Saves client's payment agent details.

## Parameters:

    
    
    args : dict with following keys
        affiliate_id : str
            [Optional] Client's My Affiliate id, if exists.
        code_of_conduct_approval : int
            Indicates client's agreement with the Code of Conduct.
        commission_deposit : Number
            Commission  (%) the agent wants to take on deposits
        commission_withdrawal : Number
            Commission  (%) the agent wants to take on withdrawals
        email : str
            Payment agent's email address.
        information : str
            [Optional] Information about payment agent and their proposed service.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        payment_agent_name : str
            The name with which the payment agent is going to be identified.
        paymentagent_create : int
            Must be 1
        phone_numbers : Any
            Payment agent's phone number(s) with country code.
        req_id : int
            [Optional] Used to map request to response.
        supported_payment_methods : Any
            A list of supported payment methods.
        urls : Any
            The URL(s) of payment agent's website(s).
    

` async def paymentagent_details(self, args=None) `

    

Gets client's payment agent details.

## Parameters:

    
    
    args : dict with following keys
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        paymentagent_details : int
            Must be 1
        req_id : int
            [Optional] Used to map request to response.
    

` async def paymentagent_list(self, args=None) `

    

Will return a list of Payment Agents for a given country for a given currency.
Payment agents allow users to deposit and withdraw funds using local payment
methods that might not be available via the main website's cashier system.

## Parameters:

    
    
    args : dict with following keys
        currency : str
            [Optional] If specified, only payment agents that supports that currency will be returned (obtained from payout_currencies call).
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        paymentagent_list : str
            Client's 2-letter country code (obtained from residence_list call).
        req_id : int
            [Optional] Used to map request to response.
    

` async def paymentagent_transfer(self, args=None) `

    

Payment Agent Transfer - this call is available only to accounts that are
approved Payment Agents.

## Parameters:

    
    
    args : dict with following keys
        amount : Number
            The amount to transfer.
        currency : str
            Currency code.
        description : str
            [Optional] Remarks about the transfer.
        dry_run : int
            [Optional] If set to 1, just do validation.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        paymentagent_transfer : int
            Must be 1
        req_id : int
            [Optional] Used to map request to response.
        transfer_to : str
            The loginid of the recipient account.
    

` async def paymentagent_withdraw(self, args=None) `

    

Initiate a withdrawal to an approved Payment Agent.

## Parameters:

    
    
    args : dict with following keys
        amount : Number
            The amount to withdraw to the payment agent.
        currency : str
            The currency code.
        description : str
            [Optional] Remarks about the withdraw. Only letters, numbers, space, period, comma, - ' are allowed.
        dry_run : int
            [Optional] If set to 1, just do validation.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        paymentagent_loginid : str
            The payment agent loginid received from the paymentagent_list call.
        paymentagent_withdraw : int
            Must be 1
        req_id : int
            [Optional] Used to map request to response.
        verification_code : str
            Email verification code (received from a verify_email call, which must be done first)
    

` async def paymentagent_withdraw_justification(self, args=None) `

    

Provide justification to perform withdrawal using a Payment Agent.

## Parameters:

    
    
    args : dict with following keys
        message : str
            Reasons for needing to withdraw using a Payment Agent.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        paymentagent_withdraw_justification : int
            Must be 1
        req_id : int
            [Optional] Used to map request to response.
    

` async def payout_currencies(self, args=None) `

    

Retrieve a list of available option payout currencies. If a user is logged in,
only the currencies available for the account will be returned.

## Parameters:

    
    
    args : dict with following keys
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        payout_currencies : int
            Must be 1
        req_id : int
            [Optional] Used to map request to response.
    

` async def ping(self, args=None) `

    

To send the ping request to the server. Mostly used to test the connection or
to keep it alive.

## Parameters:

    
    
    args : dict with following keys
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        ping : int
            Must be 1
        req_id : int
            [Optional] Used to map request to response.
    

` async def portfolio(self, args=None) `

    

Receive information about my current portfolio of outstanding options

## Parameters:

    
    
    args : dict with following keys
        contract_type : Any
            Return only contracts of the specified types
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        portfolio : int
            Must be 1
        req_id : int
            [Optional] Used to map request to response.
    

` async def profit_table(self, args=None) `

    

Retrieve a summary of account Profit Table, according to given search criteria

## Parameters:

    
    
    args : dict with following keys
        contract_type : Any
            Return only contracts of the specified types
        date_from : str
            [Optional] Start date (epoch or YYYY-MM-DD)
        date_to : str
            [Optional] End date (epoch or YYYY-MM-DD)
        description : int
            [Optional] If set to 1, will return full contracts description.
        limit : Number
            [Optional] Apply upper limit to count of transactions received.
        offset : int
            [Optional] Number of transactions to skip.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        profit_table : int
            Must be 1
        req_id : int
            [Optional] Used to map request to response.
        sort : str
            [Optional] Sort direction.
    

` async def proposal(self, args=None) `

    

Gets latest price for a specific contract.

## Parameters:

    
    
    args : dict with following keys
        amount : Number
            [Optional] Proposed contract payout or stake, or multiplier (for lookbacks).
        barrier : str
            [Optional] Barrier for the contract (or last digit prediction for digit contracts). Contracts less than 24 hours in duration would need a relative barrier (barriers which need +/-), where entry spot would be adjusted accordingly with that amount to define a barrier, except for Synthetic Indices as they support both relative and absolute barriers. Not needed for lookbacks.
        barrier2 : str
            [Optional] Low barrier for the contract (for contracts with two barriers). Contracts less than 24 hours in duration would need a relative barrier (barriers which need +/-), where entry spot would be adjusted accordingly with that amount to define a barrier, except for Synthetic Indices as they support both relative and absolute barriers. Not needed for lookbacks.
        barrier_range : str
            [Optional] Barrier range for callputspread.
        basis : str
            [Optional] Indicates type of the amount.
        cancellation : str
            Cancellation duration option (only for MULTUP and MULTDOWN contracts).
        contract_type : str
            The proposed contract type
        currency : str
            This can only be the account-holder's currency (obtained from payout_currencies call).
        date_expiry : int
            [Optional] Epoch value of the expiry time of the contract. Either date_expiry or duration is required.
        date_start : int
            [Optional] Indicates epoch value of the starting time of the contract. If left empty, the start time of the contract is now.
        duration : int
            [Optional] Duration quantity. Either date_expiry or duration is required.
        duration_unit : str
            [Optional] Duration unit - s: seconds, m: minutes, h: hours, d: days, t: ticks.
        growth_rate : Number
            [Optional] Growth rate of an accumulator contract.
        limit_order : Any
        multiplier : Number
            [Optional] The multiplier for non-binary options. E.g. lookbacks.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        product_type : str
            [Optional] The product type.
        proposal : int
            Must be 1
        req_id : int
            [Optional] Used to map request to response.
        selected_tick : int
            [Optional] The tick that is predicted to have the highest/lowest value - for TICKHIGH and TICKLOW contracts.
        subscribe : int
            [Optional] 1 - to initiate a realtime stream of prices. Note that tick trades (without a user-defined barrier), digit trades and less than 24 hours at-the-money contracts for the following underlying symbols are not streamed: R_10, R_25, R_50, R_75, R_100, RDBULL, RDBEAR (this is because their price is constant).
        symbol : str
            The short symbol name (obtained from active_symbols call).
        trading_period_start : int
            [Optional] Required only for multi-barrier trading. Defines the epoch value of the trading period start time.
    

` async def proposal_open_contract(self, args=None) `

    

Get latest price (and other information) for a contract in the user's
portfolio

## Parameters:

    
    
    args : dict with following keys
        contract_id : int
            [Optional] Contract ID received from a portfolio request. If not set, you will receive stream of all open contracts.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        proposal_open_contract : int
            Must be 1
        req_id : int
            [Optional] Used to map request to response.
        subscribe : int
            [Optional] 1 to stream.
    

` async def reality_check(self, args=None) `

    

Retrieve summary of client's trades and account for the Reality Check
facility. A 'reality check' means a display of time elapsed since the session
began, and associated client profit/loss. The Reality Check facility is a
regulatory requirement for certain landing companies.

## Parameters:

    
    
    args : dict with following keys
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        reality_check : int
            Must be 1
        req_id : int
            [Optional] Used to map request to response.
    

` async def residence_list(self, args=None) `

    

This call returns a list of countries and 2-letter country codes, suitable for
populating the account opening form.

## Parameters:

    
    
    args : dict with following keys
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        residence_list : int
            Must be 1
    

` async def revoke_oauth_app(self, args=None) `

    

Used for revoking access of particular app.

## Parameters:

    
    
    args : dict with following keys
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        revoke_oauth_app : int
            The application ID to revoke.
    

` async def sell(self, args=None) `

    

Sell a Contract as identified from a previous `portfolio` call.

## Parameters:

    
    
    args : dict with following keys
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        price : Number
            Minimum price at which to sell the contract, or 0 for 'sell at market'.
        req_id : int
            [Optional] Used to map request to response.
        sell : int
            Pass contract_id received from the portfolio call.
    

` async def sell_contract_for_multiple_accounts(self, args=None) `

    

Sell contracts for multiple accounts simultaneously. Uses the shortcode
response from `buy_contract_for_multiple_accounts` to identify the contract,
and authorisation tokens to select which accounts to sell those contracts on.
Note that only the accounts identified by the tokens will be affected. This
will not sell the contract on the currently-authorised account unless you
include the token for the current account.

## Parameters:

    
    
    args : dict with following keys
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        price : Number
            Minimum price at which to sell the contract, or 0 for 'sell at market'.
        req_id : int
            [Optional] Used to map request to response.
        sell_contract_for_multiple_accounts : int
            Must be 1
        shortcode : str
            An internal ID used to identify the contract which was originally bought. This is returned from the buy and buy_contract_for_multiple_accounts calls.
        tokens : Any
            Authorisation tokens which select the accounts to sell use for the affected accounts.
    

` async def sell_expired(self, args=None) `

    

This call will try to sell any expired contracts and return the number of sold
contracts.

## Parameters:

    
    
    args : dict with following keys
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        sell_expired : int
            Must be 1
    

` async def set_account_currency(self, args=None) `

    

Set account currency, this will be default currency for your account i.e
currency for trading, deposit. Please note that account currency can only be
set once, and then can never be changed.

## Parameters:

    
    
    args : dict with following keys
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        set_account_currency : str
            Currency of the account. List of supported currencies can be acquired with payout_currencies call.
    

` async def set_financial_assessment(self, args=None) `

    

This call sets the financial assessment details based on the client's answers
to analyze whether they possess the experience and knowledge to understand the
risks involved with binary options trading.

## Parameters:

    
    
    args : dict with following keys
        account_turnover : str
            [Optional] The anticipated account turnover.
        binary_options_trading_experience : str
            [Optional] Binary options trading experience.
        binary_options_trading_frequency : str
            [Optional] Binary options trading frequency.
        cfd_trading_experience : str
            [Optional] CFDs trading experience.
        cfd_trading_frequency : str
            [Optional] CFDs trading frequency.
        education_level : str
            [Optional] Level of Education.
        employment_industry : str
            [Optional] Industry of Employment.
        employment_status : str
            [Optional] Employment Status.
        estimated_worth : str
            [Optional] Estimated Net Worth.
        financial_information : Any
        forex_trading_experience : str
            [Optional] Forex trading experience.
        forex_trading_frequency : str
            [Optional] Forex trading frequency.
        income_source : str
            [Optional] Income Source.
        net_income : str
            [Optional] Net Annual Income.
        occupation : str
            [Optional] Occupation.
        other_instruments_trading_experience : str
            [Optional] Trading experience in other financial instruments.
        other_instruments_trading_frequency : str
            [Optional] Trading frequency in other financial instruments.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        set_financial_assessment : int
            Must be 1
        source_of_wealth : str
            [Optional] Source of wealth.
        trading_experience : Any
        trading_experience_regulated : Any
    

` async def set_self_exclusion(self, args=None) `

    

Set Self-Exclusion (this call should be used in conjunction with
`get_self_exclusion`)

## Parameters:

    
    
    args : dict with following keys
        exclude_until : Any
            [Optional] Exclude me from the website (for a minimum of 6 months, up to a maximum of 5 years). Note: uplifting this self-exclusion may require contacting the company.
        max_30day_deposit : Any
            [Optional] 7-day limit on deposits.
        max_30day_losses : Any
            [Optional] 30-day limit on losses.
        max_30day_turnover : Any
            [Optional] 30-day turnover limit.
        max_7day_deposit : Any
            [Optional] 7-day limit on deposits.
        max_7day_losses : Any
            [Optional] 7-day limit on losses.
        max_7day_turnover : Any
            [Optional] 7-day turnover limit.
        max_balance : Any
            [Optional] Maximum account cash balance.
        max_deposit : Any
            [Optional] Daily deposit limit.
        max_losses : Any
            [Optional] Daily limit on losses.
        max_open_bets : Any
            [Optional] Maximum number of open positions.
        max_turnover : Any
            [Optional] Daily turnover limit.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        session_duration_limit : Any
            [Optional] Session duration limit, in minutes.
        set_self_exclusion : int
            Must be 1
        timeout_until : Any
            [Optional] Exclude me from the website (for up to 6 weeks). Requires time in epoch format. Note: unlike exclude_until, this self-exclusion will be lifted automatically at the expiry of the timeout period.
    

` async def set_settings(self, args=None) `

    

Set User Settings (this call should be used in conjunction with
`get_settings`)

## Parameters:

    
    
    args : dict with following keys
        account_opening_reason : str
            [Optional] Purpose and reason for requesting the account opening. Only applicable for real money account. Required for clients that have not set it yet. Can only be set once.
        address_city : str
            [Optional] Note: not applicable for virtual account. Required field for real money account.
        address_line_1 : str
            [Optional] Note: not applicable for virtual account. Required field for real money account.
        address_line_2 : Any
            [Optional] Note: not applicable for virtual account. Optional field for real money account.
        address_postcode : str
            [Optional] Note: not applicable for virtual account. Optional field for real money account.
        address_state : str
            [Optional] Note: not applicable for virtual account. Optional field for real money account.
        allow_copiers : int
            [Optional] Boolean value 1 or 0, indicating permission to allow others to follow your trades. Note: not applicable for Virtual account. Only allow for real money account.
        citizen : Any
            [Optional] Country of legal citizenship, 2-letter country code.
        date_of_birth : str
            [Optional] Date of birth format: yyyy-mm-dd (can only be changed on unauthenticated svg accounts).
        dxtrade_user_exception : int
            Boolean value 1 or 0, indicating if user email belong to dxtrade exception list.
        email_consent : int
            [Optional] Boolean value 1 or 0, indicating permission to use email address for any contact which may include marketing
        employment_status : str
            [Optional] Employment Status.
        feature_flag : Any
        first_name : str
            [Optional] Within 2-50 characters, use only letters, spaces, hyphens, full-stops or apostrophes (can only be changed on unauthenticated svg accounts).
        last_name : str
            [Optional] Within 2-50 characters, use only letters, spaces, hyphens, full-stops or apostrophes (can only be changed on unauthenticated svg accounts).
        non_pep_declaration : int
            [Optional] Indicates client's self-declaration of not being a PEP/RCA (Politically Exposed Person/Relatives and Close Associates). Effective for real accounts only.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        phone : Any
            [Optional] Note: not applicable for virtual account. Starting with + followed by 9-35 digits, hyphens or space.
        place_of_birth : str
            [Optional] Place of birth, 2-letter country code.
        preferred_language : Any
            [Optional] User's preferred language, ISO standard language code
        req_id : int
            [Optional] Used to map request to response.
        request_professional_status : int
            [Optional] Required when client wants to be treated as professional. Applicable for financial accounts only.
        residence : Any
            [Optional] 2-letter country code. Note: not applicable for real money account. Only allow for Virtual account without residence set.
        salutation : str
            [Optional] Accept any value in enum list (can only be changed on unauthenticated svg accounts).
        secret_answer : str
            [Optional] Answer to secret question, within 4-50 characters. Required for new account and existing client details will be used if client opens another account.
        secret_question : str
            [Optional] Accept any value in enum list. Required for new account and existing client details will be used if client opens another account.
        set_settings : int
            Must be 1
        tax_identification_number : str
            [Optional] Tax identification number. Only applicable for real money account. Required for maltainvest landing company.
        tax_residence : str
            [Optional] Residence for tax purpose. Comma separated iso country code if multiple jurisdictions. Only applicable for real money account. Required for maltainvest landing company.
        trading_hub : int
            [Optional] Enable/Disable Trading Hub dashboard
    

` async def statement(self, args=None) `

    

Retrieve a summary of account transactions, according to given search criteria

## Parameters:

    
    
    args : dict with following keys
        action_type : str
            [Optional] To filter the statement according to the type of transaction.
        date_from : int
            [Optional] Start date (epoch)
        date_to : int
            [Optional] End date (epoch)
        description : int
            [Optional] If set to 1, will return full contracts description.
        limit : Number
            [Optional] Maximum number of transactions to receive.
        offset : int
            [Optional] Number of transactions to skip.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        statement : int
            Must be 1
    

` async def states_list(self, args=None) `

    

For a given country, returns a list of States of that country. This is useful
to populate the account opening form.

## Parameters:

    
    
    args : dict with following keys
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        states_list : str
            Client's 2-letter country code (obtained from residence_list call)
    

` async def ticks(self, args=None) `

    

Initiate a continuous stream of spot price updates for a given symbol.

## Parameters:

    
    
    args : dict with following keys
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        subscribe : int
            [Optional] If set to 1, will send updates whenever a new tick is received.
        ticks : Any
            The short symbol name or array of symbols (obtained from active_symbols call).
    

` async def ticks_history(self, args=None) `

    

Get historic tick data for a given symbol.

    
    
        Parameters:
        -----------
            args : dict with following keys
                adjust_start_time : int
                    [Optional] 1 - if the market is closed at the end time, or license limit is before end time, adjust interval backwards to compensate.
                count : int
                    [Optional] An upper limit on ticks to receive.
                end : str
                    Epoch value representing the latest boundary of the returned ticks. If latest is specified, this will be the latest available timestamp.
                granularity : int
                    [Optional] Only applicable for style: candles. Candle time-dimension width setting. (default: 60).
                passthrough : Any
                    [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
                req_id : int
                    [Optional] Used to map request to response.
                start : int
                    [Optional] Epoch value representing the earliest boundary of the returned ticks.
    

  * For "style": "ticks": this will default to 1 day ago.
  * For "style": "candles": it will default to 1 day ago if count or granularity is undefined. style : str [Optional] The tick-output style. subscribe : int [Optional] 1 - to send updates whenever a new tick is received. ticks_history : str Short symbol name (obtained from the active_symbols call).

` async def time(self, args=None) `

    

Request back-end server epoch time.

## Parameters:

    
    
    args : dict with following keys
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        time : int
            Must be 1
    

` async def tnc_approval(self, args=None) `

    

To approve the latest version of terms and conditions.

## Parameters:

    
    
    args : dict with following keys
        affiliate_coc_agreement : int
            [Optional] For Affiliate's Code of Conduct Agreement.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        tnc_approval : Number
            Must be 1
        ukgc_funds_protection : int
            [Optional] For ASK_UK_FUNDS_PROTECTION in cashier.
    

` async def topup_virtual(self, args=None) `

    

When a virtual-money's account balance becomes low, it can be topped up using
this call.

## Parameters:

    
    
    args : dict with following keys
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        topup_virtual : int
            Must be 1
    

` async def trading_durations(self, args=None) `

    

Retrieve a list of all available underlyings and the corresponding contract
types and trading duration boundaries. If the user is logged in, only the
assets available for that user's landing company will be returned.

## Parameters:

    
    
    args : dict with following keys
        landing_company : str
            Deprecated - Replaced by landing_company_short.
        landing_company_short : str
            [Optional] If specified, will return only the underlyings for the specified landing company.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        trading_durations : int
            Must be 1
    

` async def trading_platform_investor_password_reset(self, args=None) `

    

Reset the investor password of a Trading Platform Account

## Parameters:

    
    
    args : dict with following keys
        account_id : str
            Trading account ID.
        new_password : str
            New password of the account. For validation (Accepts any printable ASCII character. Must be within 8-25 characters, and include numbers, lowercase and uppercase letters. Must not be the same as the user's email address).
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        platform : str
            Name of trading platform.
        req_id : int
            [Optional] Used to map request to response.
        trading_platform_investor_password_reset : int
            Must be 1
        verification_code : str
            Email verification code (received from a verify_email call, which must be done first)
    

` async def trading_platform_password_reset(self, args=None) `

    

Reset the password of a Trading Platform Account

## Parameters:

    
    
    args : dict with following keys
        new_password : str
            New password of the account. For validation (Accepts any printable ASCII character. Must be within 8-25 characters, and include numbers, lowercase and uppercase letters. Must not be the same as the user's email address).
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        platform : str
            Name of trading platform.
        req_id : int
            [Optional] Used to map request to response.
        trading_platform_password_reset : int
            Must be 1
        verification_code : str
            Email verification code (received from a verify_email call, which must be done first)
    

` async def trading_servers(self, args=None) `

    

Get the list of servers for a trading platform.

## Parameters:

    
    
    args : dict with following keys
        account_type : str
            [Optional] Trading account type.
        environment : str
            [Optional] Pass the environment (installation) instance. Currently, there are one demo and two real environments. Defaults to 'all'.
        market_type : str
            [Optional] Market type.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        platform : str
            [Optional] Pass the trading platform name, default to mt5
        req_id : int
            [Optional] Used to map request to response.
        trading_servers : int
            Must be 1
    

` async def trading_times(self, args=None) `

    

Receive a list of market opening times for a given date.

## Parameters:

    
    
    args : dict with following keys
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        trading_times : str
            Date to receive market opening times for. (yyyy-mm-dd format. today can also be specified).
    

` async def transaction(self, args=None) `

    

Subscribe to transaction notifications

## Parameters:

    
    
    args : dict with following keys
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        subscribe : int
            If set to 1, will send updates whenever there is an update to transactions. If not to 1 then it will not return any records.
        transaction : int
            Must be 1
    

` async def transfer_between_accounts(self, args=None) `

    

This call allows transfers between accounts held by a given user. Transfer
funds between your fiat and cryptocurrency accounts (for a fee). Please note
that account_from should be same as current authorized account.

## Parameters:

    
    
    args : dict with following keys
        account_from : str
            [Optional] The loginid of the account to transfer funds from.
        account_to : str
            [Optional] The loginid of the account to transfer funds to.
        accounts : str
            [Optional] To control the list of accounts returned when account_from or account_to is not provided. brief (default value) means that accounts with mt5 account_type will be excluded; it will run faster. all means that all accounts with any account_type (including mt5) will be returned.
        amount : Number
            [Optional] The amount to transfer.
        currency : str
            [Optional] Currency code.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        transfer_between_accounts : int
            If account_from or account_to is not provided, it just returns the available accounts.
    

` async def unsubscribe_email(self, args=None) `

    

It unsubscribe user from the email subscription.

## Parameters:

    
    
    args : dict with following keys
        binary_user_id : Number
            Customer User ID.
        checksum : str
            The generated checksum for the customer.
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        unsubscribe_email : int
            Must be 1
    

` async def verify_email(self, args=None) `

    

Verify an email address for various purposes. The system will send an email to
the address containing a security code for verification.

## Parameters:

    
    
    args : dict with following keys
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        type : str
            Purpose of email verification, request_email and reset_password are the only two types restricted from all unoffical apps
        url_parameters : Any
        verify_email : str
            Email address to be verified.
    

` async def verify_email_cellxpert(self, args=None) `

    

Verify an email address for Cellxpert. The system will send an email to the
address containing a security code for verification.

## Parameters:

    
    
    args : dict with following keys
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        type : str
            Purpose of the email verification call.
        url_parameters : Any
        verify_email_cellxpert : str
            Email address to be verified.
    

` async def website_status(self, args=None) `

    

Request server status.

## Parameters:

    
    
    args : dict with following keys
        passthrough : Any
            [Optional] Used to pass data through the websocket, which may be retrieved via the echo_req output field. Maximum size is 3500 bytes.
        req_id : int
            [Optional] Used to map request to response.
        subscribe : int
            [Optional] 1 to stream the server/website status updates.
        website_status : int
            Must be 1
    

# Index

  * ### Super-module

    * `[deriv_api](index.html "deriv_api")`
  * ### Classes

    * #### `DerivAPICalls`

      * `active_symbols`
      * `api_token`
      * `app_delete`
      * `app_get`
      * `app_list`
      * `app_markup_details`
      * `app_markup_statistics`
      * `app_register`
      * `app_update`
      * `asset_index`
      * `authorize`
      * `balance`
      * `buy`
      * `buy_contract_for_multiple_accounts`
      * `cancel`
      * `cashier`
      * `contract_update`
      * `contract_update_history`
      * `contracts_for`
      * `copy_start`
      * `copy_stop`
      * `copytrading_list`
      * `copytrading_statistics`
      * `crypto_config`
      * `document_upload`
      * `economic_calendar`
      * `exchange_rates`
      * `forget`
      * `forget_all`
      * `get_account_status`
      * `get_financial_assessment`
      * `get_limits`
      * `get_self_exclusion`
      * `get_settings`
      * `identity_verification_document_add`
      * `kyc_auth_status`
      * `landing_company`
      * `landing_company_details`
      * `login_history`
      * `logout`
      * `mt5_deposit`
      * `mt5_get_settings`
      * `mt5_login_list`
      * `mt5_new_account`
      * `mt5_password_change`
      * `mt5_password_check`
      * `mt5_password_reset`
      * `mt5_withdrawal`
      * `new_account_maltainvest`
      * `new_account_real`
      * `new_account_virtual`
      * `oauth_apps`
      * `p2p_advert_create`
      * `p2p_advert_info`
      * `p2p_advert_list`
      * `p2p_advert_update`
      * `p2p_advertiser_adverts`
      * `p2p_advertiser_create`
      * `p2p_advertiser_info`
      * `p2p_advertiser_list`
      * `p2p_advertiser_payment_methods`
      * `p2p_advertiser_relations`
      * `p2p_advertiser_update`
      * `p2p_chat_create`
      * `p2p_order_cancel`
      * `p2p_order_confirm`
      * `p2p_order_create`
      * `p2p_order_dispute`
      * `p2p_order_info`
      * `p2p_order_list`
      * `p2p_order_review`
      * `p2p_payment_methods`
      * `p2p_ping`
      * `payment_methods`
      * `paymentagent_create`
      * `paymentagent_details`
      * `paymentagent_list`
      * `paymentagent_transfer`
      * `paymentagent_withdraw`
      * `paymentagent_withdraw_justification`
      * `payout_currencies`
      * `ping`
      * `portfolio`
      * `profit_table`
      * `proposal`
      * `proposal_open_contract`
      * `reality_check`
      * `residence_list`
      * `revoke_oauth_app`
      * `sell`
      * `sell_contract_for_multiple_accounts`
      * `sell_expired`
      * `set_account_currency`
      * `set_financial_assessment`
      * `set_self_exclusion`
      * `set_settings`
      * `statement`
      * `states_list`
      * `ticks`
      * `ticks_history`
      * `time`
      * `tnc_approval`
      * `topup_virtual`
      * `trading_durations`
      * `trading_platform_investor_password_reset`
      * `trading_platform_password_reset`
      * `trading_servers`
      * `trading_times`
      * `transaction`
      * `transfer_between_accounts`
      * `unsubscribe_email`
      * `verify_email`
      * `verify_email_cellxpert`
      * `website_status`

Generated by [pdoc 0.10.0](https://pdoc3.github.io/pdoc "pdoc: Python API
documentation generator").



---

## Documentation from [https://deriv-com.github.io/python-deriv-api/in_memory.html](https://deriv-com.github.io/python-deriv-api/in_memory.html)

# Module `deriv_api.in_memory`

## Classes

` class InMemory `

    

An in memory storage which can be used for caching

# Index

  * ### Super-module

    * `[deriv_api](index.html "deriv_api")`
  * ### Classes

    * #### `InMemory`

Generated by [pdoc 0.10.0](https://pdoc3.github.io/pdoc "pdoc: Python API
documentation generator").



---

## Documentation from [https://deriv-com.github.io/python-deriv-api/middlewares.html](https://deriv-com.github.io/python-deriv-api/middlewares.html)

# Module `deriv_api.middlewares`

## Classes

` class MiddleWares (middlewares={}) `

    

A class that help to manage middlewares

## Examples

middlewares = MiddleWares() middlewares.add('sendWillBeCalled', lanmbda req:
print(req)) middlewares = Middlewares({'sendWillBeCalled': lambda req:
print(req)}) middleware->call('sendWillBeCalled', arg1, arg2)

## Parameters

options: dict with following key value pairs key: string, middleware name
value: function, middleware code

### Methods

` def add(self, name, code) `

    

Add middleware

## Parameters

name: Str middleware name code: function middleware code

` def call(self, name, args) `

    

Call middleware and return the result if there is such middleware

## Parameters

**`name`** : `string`

     
**`args`** : `list`

    the args that will feed to middleware

## Returns

    
    
    If there is such middleware, then return the result of middleware
    else return None
    

# Index

  * ### Super-module

    * `[deriv_api](index.html "deriv_api")`
  * ### Classes

    * #### `MiddleWares`

      * `add`
      * `call`

Generated by [pdoc 0.10.0](https://pdoc3.github.io/pdoc "pdoc: Python API
documentation generator").



---

## Documentation from [https://deriv-com.github.io/python-deriv-api/streams_list.html](https://deriv-com.github.io/python-deriv-api/streams_list.html)

# Module `deriv_api.streams_list`

# Index

  * ### Super-module

    * `[deriv_api](index.html "deriv_api")`

Generated by [pdoc 0.10.0](https://pdoc3.github.io/pdoc "pdoc: Python API
documentation generator").



---

## Documentation from [https://deriv-com.github.io/python-deriv-api/subscription_manager.html](https://deriv-com.github.io/python-deriv-api/subscription_manager.html)

# Module `deriv_api.subscription_manager`

## Classes

` class SubscriptionManager (api) `

    

Subscription Manager - manage subscription channels

Makes sure there is always only one subscription channel for all requests of
subscriptions, keeps a history of received values for the subscription of
ticks and forgets channels that do not have subscribers. It also ensures that
subscriptions are revived after connection drop/account changed.

## Parameters

    
    
    api : deriv_api.DerivAPI
    

## Example

  * create a new subscription for R_100

    
    
    >>> source_tick_50: Observable  = await api.subscribe({'ticks': 'R_50'})
    >>> subscription_id = 0
    >>> def tick_50_callback(data):
    >>>     global subscription_id
    >>>     subscription_id = data['subscription']['id']
    >>>     print(data)
    >>> source_tick_50.subscribe(tick_50_callback)
    

  * forget all ticks

    
    
    >>> await api.forget_all('ticks')
    

  * forget based on subscription id

    
    
    >>> await api.forget(subscription_id)
    

### Methods

` async def subscribe(self, request) `

    

Subscribe to a given request, returns a stream of new responses, Errors should
be handled by the user of the stream

## Example

    
    
    >>> ticks = api.subscribe({ 'ticks': 'R_100' })
    >>> ticks.subscribe(call_back_function)
    

## Parameters

**`request`** : `dict`

    A request object acceptable by the API

## Returns

    
    
    Observable
        An RxPY SObservable
    

# Index

  * ### Super-module

    * `[deriv_api](index.html "deriv_api")`
  * ### Classes

    * #### `SubscriptionManager`

      * `subscribe`

Generated by [pdoc 0.10.0](https://pdoc3.github.io/pdoc "pdoc: Python API
documentation generator").



---

## Documentation from [https://api.deriv.com/api-explorer](https://api.deriv.com/api-explorer)

Skip to main content

[![Deriv API logo](/img/derivlogo.svg)](/)[API explorer](/api-
explorer)[Documentation](https://developers.deriv.com)[Deriv
tech](https://tech.deriv.com/)[Bug
bounty](https://hackerone.com/deriv?type=team)

Log inSign up

EN

  * English
  * Français

[Home](/)[API explorer](/api-explorer)

## API Explorer

Select API Call - Version 3

Request JSON

Send request

Clear response

###### API

  * [Dashboard](/dashboard)
  * [API explorer](/api-explorer)
  * [Documentation](https://developers.deriv.com)
  * [Deriv Tech](https://deriv.com/derivtech)
  * [Bug bounty](https://hackerone.com/deriv?type=team)

###### Deriv.com

  * [Homepage](https://deriv.com/)
  * [Who we are](https://deriv.com/who-we-are)
  * [Contact us](https://deriv.com/contact-us)

### API

### Deriv.com

##### Get connected

Discuss ideas and share solutions with developers worldwide.

Join our communityTelegram

##### We're here to help

Email us at

[api-support@deriv.com ](mailto:api-support@deriv.com)

if you need any assistance or support.

Send an email

![](https://www.facebook.com/tr?id=780746632361102&ev=PageView&noscript=1)

