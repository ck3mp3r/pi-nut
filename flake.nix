{
  description = "virtual environments";

  inputs.devshell.url = "github:numtide/devshell";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, flake-utils, devshell, nixpkgs }:
    flake-utils.lib.eachDefaultSystem (system: {
      devShell =
        let
          pkgs = import nixpkgs {
            inherit system;
            config.allowUnfree = true;
            config.allowBroken = true;
            overlays = [ devshell.overlay ];
          };
        in
        pkgs.devshell.mkShell {
          imports = [ (pkgs.devshell.extraModulesDir + "/git/hooks.nix") ];
          git.hooks.enable = true;
          # git.hooks.pre-commit.text = "./misc/git-hooks/pre-commit";
          motd = "";
          packages = with pkgs;[
            ansible
            delve
            go
            inetutils
            podman
            podman-tui
            python39
            python39Packages.virtualenv
            qemu
          ];

          devshell.startup.setup_sdk_path.text = ''
            if [ ! -d .venv ]; then
              virtualenv .venv
              source .venv/bin/activate;
              pip3 install -r ./src/python/server/requirements.txt
              pip3 install -r ./src/python/dispenser/requirements.txt
            else
              source .venv/bin/activate;
            fi
          '';
        };
    });
}

