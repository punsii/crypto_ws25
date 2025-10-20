{
  description = "Kryptographie";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    treefmt-nix.url = "github:numtide/treefmt-nix";
  };
  outputs =
    {
      nixpkgs,
      treefmt-nix,
      ...
    }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfree = true;
      };
      treefmtEval = treefmt-nix.lib.evalModule pkgs {
        # Used to find the project root
        projectRootFile = "flake.nix";

        programs = {
          black.enable = true;
          isort.enable = true;
          prettier.enable = true;
          nixfmt.enable = true;
        };
        settings.formatter.black.includes = [ "*.sage" ];
      };
      extraPythonPackages =
        ps: with ps; [
          pytest
          pycryptodome
        ];

      sage = pkgs.sage.override {
        requireSageTests = false;
        inherit extraPythonPackages;
      };
      sagelib = sage.with-env.env.lib;

      python3 = pkgs.python3 // {
        pkgs = pkgs.python3.pkgs.overrideScope (
          self: super: {
            inherit sagelib;
          }
        );
      };
      pythonEnv = python3.withPackages (ps: (extraPythonPackages ps) ++ [ sagelib ]);

    in
    {
      packages.${system} = {
        default = pkgs.dockerTools.buildLayeredImage {
          name = "sage";
          tag = "latest";
          created = "now";
          contents = [ sage ];
        };
      };

      devShells.${system}.default = pkgs.mkShell {
        packages = [
          treefmtEval.config.build.wrapper
          pythonEnv
          sage
        ];
      };

      formatter.${system} = treefmtEval.config.build.wrapper;
    };
}
