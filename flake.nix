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
      };
      pythonEnv = pkgs.python3.withPackages (
        ps: with ps; [
          matplotlib
          numpy
          pandas
          streamlit
        ]
      );
    in
    {
      packages.${system} = rec {
        inherit pythonEnv;
        default = pythonEnv;
      };

      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [ 
          treefmtEval.config.build.wrapper
          pythonEnv
          sage
        ];
      };

      formatter.${system} = treefmtEval.config.build.wrapper;
    };
}
