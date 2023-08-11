
# net-registry-index

#### Net Stalker's private rust package registry for maintaining organization's crates.

How to download packages from this registry?

1. Modify `.cargo/config.toml` in the cargo workspace. Add the following lines

```
[registries]
net-registry = { index = "https://github.com/net-stalker/net-registry-index.git" }
```
Use only `https` because Cargo, the Rust package manager, does not directly support `SSH` URLs for specifying registries in the `.cargo/config.toml` file. Cargo primarily uses `HTTPS` URLs for accessing registries.

2. Add you first dependency

To add your first dependency just write the following in your `Cargo.toml`:
```
package-name = { version = "0.1.0", registry = "net-registry" }
```

3. How to let cargo get access to github private repo? 

First off all you need to generate you personal access token (PAT further). I higly reccomend you to use github official documentaion to do so [how to generate PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic). **Don't forget to save it in a secure place!**

4. Download the packages

After you have modified `Cargo.toml` and generated PAT the next step you need to do is to run this command in your working directory:

```
cargo update
```
After that you will be prompted to write your username and password to the registry (in this case your github username and PAT). Then if you do everything correctly your git credentials will be saved in 
`$HOME/.git-credentials` and all the packages will be dowloaded from the registry.

***Happy coding!***


## Authors

- [Illia Stetsenko(net-illia-stetsenko)](https://github.com/net-illia-stetsenko)

