<br/>
<br/>

<div  align="center"> <p > <img src="https://raw.githubusercontent.com/terra-project/terra-sdk-python/main/docs/img/logo.png" width=500 alt="py-sdk-logo"></p>


The Python SDK for Terra
<br/>
<p><sub>(Unfamiliar with Terra?  <a href="https://docs.terra.money/">Check out Terra Docs</a>)</sub></p>

  <p > <img alt="GitHub" src="https://img.shields.io/github/license/terra-project/terra-sdk-python">
<img alt="Python" src="https://img.shields.io/pypi/pyversions/terra-sdk">
  <img alt="pip" src="https://img.shields.io/pypi/v/terra-sdk"></p>
<p>
  <a href="https://terra-project.github.io/terra-sdk-python/index.html"><strong>Explore the Docs »</strong></a>
<br/>
  <a href="https://pypi.org/project/terra-sdk/">PyPI Package</a>
  ·
  <a href="https://github.com/terra-project/terra-sdk-python">GitHub Repository</a>
</p></div>


The Terra Software Development Kit (SDK) in Python is a simple library toolkit for building software that can interact with the Terra blockchain and provides simple abstractions over core data structures, serialization, key management, and API request generation.

## Features

- Written in Python offering extensive support libraries
- Versatile support for key management solutions
- Exposes the Terra API through LCDClient

<br/>

# Table of Contents
- [API Reference](#api-reference)
- [Getting Started](#getting-started)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Dependencies](#dependencies)
  - [Tests](#tests)
  - [Code Quality](#code-quality)
- [Usage Examples](#usage-examples) 
  - [Getting Blockchain Information](#getting-blockchain-information)
    - [Async Usage](#async-usage)
  - [Building and Signing Transactions](#building-and-signing-transactions)
      - [Example Using a Wallet](#example-using-a-wallet-recommended)
- [Contributing](#contributing)
  - [Reporting an Issue](#reporting-an-issue)
  - [Requesting a Feature](#requesting-a-feature)
  - [Contributing Code](#contributing-code)
  - [Documentation Contributions](#documentation-contributions)
- [License](#license)

<br/>



# API Reference
An intricate reference to the APIs on the Terra SDK can be found <a href="https://terra-project.github.io/terra-sdk-python/index.html">here</a>.

<br/>

# Getting Started
A walk-through of the steps to get started with the Terra SDK alongside with a few use case examples are provided below. Alternatively, a tutorial video is also available <a href="https://www.youtube.com/watch?v=GfasBlJHKIg">here</a> as reference.

## Requirements
Terra SDK requires <a href="https://www.python.org/downloads/">Python v3.7+</a>.

## Installation

<sub>**NOTE:** *All code starting with a `$` is meant to run on your terminal (a bash prompt). All code starting with a `>>>` is meant to run in a python interpreter, like <a href="https://pypi.org/project/ipython/">ipython</a>.*</sub>

Terra SDK can be installed (preferably in a `virtual environment` from PyPI using `pip`) as follows:

```
$ pip install -U terra_sdk
```
<sub>*You might have `pip3` installed instead of `pip`; proceed according to your own setup.*<sub>

## Dependencies
Terra SDK uses <a href="https://python-poetry.org/">Poetry</a> to manage dependencies. To get set up with all the required dependencies, run:
```
$ pip install poetry
$ poetry install
```


## Tests
Terra SDK provides extensive tests for data classes and functions. To run them, after the steps in [Dependencies](#dependencies):
```
$ make test
```

## Code Quality
Terra SDK uses <a href="https://black.readthedocs.io/en/stable/">Black</a>, <a href="https://isort.readthedocs.io/en/latest/">isort</a>, and <a href="https://mypy.readthedocs.io/en/stable/index.html">Mypy</a> for checking code quality and maintaining style. To reformat, after the steps in [Dependencies](#dependencies):
```
$ make qa && make format
```

<br/>

# Usage Examples
Terra SDK can help you read block data, sign and send transactions, deploy and interact with contracts, and many more.
Following examples are provided to help get building started; use cases and functionalities of the Terra SDK are not limited to the following examples and can be found in full <a href="https://terra-project.github.io/terra-sdk-python/index.html">here</a>.

In order to interact with the Terra blockchain, you'll need a connection to a Terra node. This can be done through setting up an LCDClient (The LCDClient is an object representing an HTTP connection to a Terra LCD node.):

```
>>> from terra_sdk.client.lcd import LCDClient
>>> terra = LCDClient(chain_id="columbus-4", url="https://lcd.terra.dev")
```

## Getting Blockchain Information

Once properly configured, the `LCDClient` instance will allow you to interact with the Terra blockchain. Try getting the latest block height:


```
>>> terra.tendermint.block_info()['block']['header']['height']
```

`'1687543'`


### Async Usage

If you want to make asynchronous, non-blocking LCD requests, you can use AsyncLCDClient. The interface is similar to LCDClient, except the module and wallet API functions must be awaited.

<pre><code>
>>> import asyncio 
>>> from terra_sdk.client.lcd import AsyncLCDClient

>>> async def main():
      <strong>terra = AsyncLCDClient("https://lcd.terra.dev", "columbus-4")</strong>
      total_supply = await terra.supply.total()
      print(total_supply)
      <strong>await terra.session.close # you must close the session</strong>

>>> asyncio.get_event_loop().run_until_complete(main())
</code></pre>

## Building and Signing Transactions

If you wish to perform a state-changing operation on the Terra blockchain such as sending tokens, swapping assets, withdrawing rewards, or even invoking functions on smart contracts, you must create a **transaction** and broadcast it to the network.
Terra SDK provides functions that help create StdTx objects.

### Example Using a Wallet (*recommended*)

A `Wallet` allows you to create and sign a transaction in a single step by automatically fetching the latest information from the blockchain (chain ID, account number, sequence).

Use `LCDClient.wallet()` to create a Wallet from any Key instance. The Key provided should correspond to the account you intend to sign the transaction with.


```
>>> from terra_sdk.client.lcd import LCDClient
>>> from terra_sdk.key.mnemonic import MnemonicKey

>>> mk = MnemonicKey(mnemonic=MNEMONIC) 
>>> terra = LCDClient("https://lcd.terra.dev", "columbus-4")
>>> wallet = terra.wallet(mk)
```

Once you have your Wallet, you can simply create a StdTx using `Wallet.create_and_sign_tx`.


```
>>> from terra_sdk.core.auth import StdFee
>>> from terra_sdk.core.bank import MsgSend

>>> tx = wallet.create_and_sign_tx(
        msgs=[MsgSend(
            wallet.key.acc_address,
            RECIPIENT,
            "1000000uluna"    # send 1 luna
        )],
        memo="test transaction!",
        fee=StdFee(200000, "120000uluna")
    )
```

You should now be able to broadcast your transaction to the network.

```
>>> result = terra.tx.broadcast(tx)
>>> print(result)
```

<br/>

# Contributing

Community contribution, whether it's a new feature, correction, bug report, additional documentation, or any other feedback is always welcome. Please read through this section to ensure that your contribution is in the most suitable format for us to effectively process.

<br/>

## Reporting an Issue 
First things first: **Do NOT report security vulnerabilities in public issues!** Please disclose responsibly by letting the <a href="mailto:william@terra.money">Terra SDK team</a> know upfront. We will assess the issue as soon as possible on a best-effort basis and will give you an estimate for when we have a fix and release available for an eventual public disclosure. </br>
If you encounter a different issue with the Python SDK, check first to see if there is an existing issue on the <a href="https://github.com/terra-project/terra-sdk-python/issues">Issues</a> page or a pull request on the <a href="https://github.com/terra-project/terra-sdk-python/pulls">Pull requests</a> page (both Open and Closed tabs) addressing the topic.

If there isn't a discussion on the topic there, you can file an issue. The ideal report includes:

* A description of the problem / suggestion.
* How to recreate the bug.
* If relevant, including the versions of your:
    * Python interpreter
    * Terra SDK
    * Optionally of the other dependencies involved
* If possible, create a pull request with a (failing) test case demonstrating what's wrong. This makes the process for fixing bugs quicker & gets issues resolved sooner.
</br>

## Requesting a Feature
If you wish to request the addition of a feature, please first checkout the <a href="https://github.com/terra-project/terra-sdk-python/issues">Issues</a> page and the <a href="https://github.com/terra-project/terra-sdk-python/pulls">Pull requests</a> page (both Open and Closed tabs). If you decide to continue with the request, think of the merits of the feature to convince the project's developers, and provide as much detail and context as possible in the form of filing an issue on the <a href="https://github.com/terra-project/terra-sdk-python/issues">Issues</a> page.


<br/>

## Contributing Code
If you wish to contribute to the repository in the form of patches, improvements, new features, etc., first scale the contribution. If it is a major development, like implementing a feature, it is recommended that you consult with the developers of the project before starting the development in order not to risk spending a lot of time working on a change that might not get merged into the project. Once confirmed, you are welcome to submit your pull request.
</br>

### For new contributors, here is a quick guide: 

1. Fork the repository.
2. Build the project using the [Dependencies](#dependencies) and [Tests](#tests) steps.
3. Install a <a href="https://virtualenv.pypa.io/en/latest/index.html">virtualenv</a>.
4. Develop your code and test the changes using the [Tests](#tests) and [Code Quality](#code-quality) steps.
5. Commit your changes (ideally follow the <a href="https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit">Angular commit message guidelines</a>).
6. Push your fork and submit a pull request to the repository's `main` branch to propose your code.
   

A good pull request:
* is clear.
* works across all supported versions of Python. (3.7+)
* Follows the existing style of the code base (<a href="https://pypi.org/project/flake8/">`Flake8`</a>).
* Has comments included as needed.
* A test case that demonstrates the previous flaw that now passes with the included patch, or demonstrates the newly added feature.
* If it adds / changes a public API, it must also include documentation for those changes.
* Must be appropriately licensed (MIT License).
</br>

## Documentation Contributions
Documentation improvements are always welcome. The documentation files live in the [docs](./docs) directory of the repository and are written in <a href="https://docutils.sourceforge.io/rst.html">reStructuredText</a> and use <a href="https://www.sphinx-doc.org/en/master/">Sphinx</a> to create the full suite of documentation.
</br>
When contributing documentation, please do your best to follow the style of the documentation files. This means a soft-limit of 88 characters wide in your text files and a semi-formal, yet friendly and approachable, prose style. You can propose your imporvements by submiting a pull request as explained above.

### Need more information on how to contribute?
You can give this <a href="https://opensource.guide/how-to-contribute/#how-to-submit-a-contribution">guide</a> read for more insight.




<br/>

# License

This software is licensed under the MIT license. See [LICENSE](./LICENSE) for full disclosure.

© 2021 Terraform Labs, PTE.

<hr/>

<p>&nbsp;</p>
<p align="center">
    <a href="https://terra.money/"><img src="https://terra.money/logos/terra_logo.svg" alt="Terra-logo" width=200/></a>
<div align="center">
  <sub><em>Powering the innovation of money.</em></sub>
</div>