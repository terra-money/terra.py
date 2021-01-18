<p>&nbsp;</p>
<p align="center">
<a href="https://terra_sdk.terra.money/">
<img src="https://terra_sdk.terra.money/img/logo.svg"/>
</a>
</p>

<h1 align="center">Terra Python SDK</h1>
<p align="center">
The Python SDK for Terra.</p>

<br/>

![diagram](./img/terra_sdk-diagram.png)

<div align="center">
  <h3>
    <a href="https://terra_sdk.terra.money/docs">
      Docs
    </a>
    <span> | </span>
    <a href="https://terra_sdk.terra.money/examples">
      Examples
    </a>
    <!--<a href="https://terra_sdk.terra.money/devguide">
      Dev Guide
    </a>-->
    <span> | </span>
    <a href="https://github.com/terra-project/terra_sdk/blob/master/CONTRIBUTING.md">
      Contributing
    </a>
  </h3>
</div>

## Installation

terra_sdk requires **Python 3.7+**. Install the latest version of terra_sdk with `pip` on PyPI:

```bash
$ pip install -U terra_sdk
```

## Pretty Printing

Many objects in terra_sdk are pretty-printable by their `._pp` property.

<pre>
        <div align="left">
        Python 3.7.6 (default, Dec 30 2019, 19:38:26)
        >>> <strong>from terra_sdk import Terra</strong>
        >>> terra = Terra("columbus-3", "https://lcd.terra.dev/")
        >>> terra.market.params()._pp
        ╒═════════════════════════╤═════════════════╕
        │ pool_recovery_period    │ 14400           │
        ├─────────────────────────┼─────────────────┤
        │ base_pool               │ 250000000000    │
        ├─────────────────────────┼─────────────────┤
        │ min_spread              │ 0.02            │
        ├─────────────────────────┼─────────────────┤
        │ tobin_tax               │ 0.0025          │
        ├─────────────────────────┼─────────────────┤
        │ illiquid_tobin_tax_list │ ╒══════╤══════╕ │
        │                         │ │ umnt │ 0.02 │ │
        │                         │ ╘══════╧══════╛ │
        ╘═════════════════════════╧═════════════════╛
        </div>
</pre>

works by default in Jupyter ...

![jupyter](https://github.com/terra-project/terra_sdk/blob/master/img/jupyter.png?raw=true)

## My First Transaction

### Connect to Soju testnet

Once you've installed terra_sdk, fire up an interactive Python shell and connect to the Soju testnet using the official Soju node provided by Terraform Labs.

```python
from terra_sdk import Terra

soju = Terra("soju-0013", "https://soju-lcd.terra.dev")
assert soju.is_connected()
```

#### Create an account

Before we can make any transactions, we have to have an account. Enter in the above to create an account and print its account address.

```python
from terra_sdk.key.mnemonic import MnemonicKey

wallet = soju.wallet(MnemonicKey.generate())
wallet.address
# terra17w4ppj92dwdf93jjtply08nav2ldzw3z2l3wzl
```

#### Top off with testnet funds

Great, now that we have an address, let's get some testnet funds. Head over to the [Soju Faucet](https://faucet.terra.money/) and top off some Luna.

<p align="center">
<img src="https://terra_sdk.terra.money/img/faucet.png" aligned="center" width="650"/>
</p>

After that's done, you should have 10,000 LUNA in your account. To confirm this, you can enter the following:

```python
wallet.balance("uluna")
# Coin('uluna', 10000000000)
```

#### Create a transaction

Let's send 23 Testnet Luna to your friend at the following address:

`terra1wg2mlrxdmnnkkykgqg4znky86nyrtc45q336yv`

We'll need to create a transaction containing a `MsgSend` alongside a short memo (note) "Hello terra_sdk!" -- our version of Hello World.

```python
from terra_sdk.core import Coins, StdFee
from terra_sdk.core.msg import MsgSend

send = MsgSend(
    from_address=wallet.address,
    to_address="terra1wg2mlrxdmnnkkykgqg4znky86nyrtc45q336yv",
    amount=Coins(uluna=23_000_000)
)

fee = StdFee.make(50000, uluna=1000) # include a small fee..

tx = wallet.create_and_sign_tx(send, memo="Hello terra_sdk!", fee=fee)
res = wallet.broadcast(tx)
```

#### See it on the blockchain

It should take around 6 seconds to finalize. If everything went well, you should get a result object with the height and TX hash after about 6 seconds.

```python
print(f"TX Hash: {res.txhash}")
# TX Hash: 82D5440A4C4CAB5B74EE3C98CE7F755372CD92E945425A572654179A4A0EE678
```

Copy the TX hash and enter it on [Finder](https://finder.terra.money/), selecting the chain `soju-0013`.

<p align="center">
<img src="https://terra_sdk.terra.money/img/txhash.png" aligned="center" width="650"/>
</p>

## Learn more

Check out the official documentation at https://terra_sdk.terra.money.

## License

This software is licensed under the MIT license. See [LICENSE](./LICENSE) for full disclosure.

© 2020 Terraform Labs, PTE.

<hr/>

<p>&nbsp;</p>
<p align="center">
    <a href="https://terra.money/"><img src="http://terra.money/logos/terra_logo.svg" align="center" width=200/></a>
</p>
<div align="center">
  <sub><em>Powering the innovation of money.</em></sub>
</div>
