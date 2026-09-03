group = "app.brave.nightly"

patches {
    about {
        name = "Brave Nightly Origin Patch"
        description = "Brave Nightly Origin patch for Morphe"
        author = "dh6k"
        website = "https://github.com/dh6k/morphe-patches"
        source = "git@github.com:dh6k/morphe-patches"
        contact = ""
        license = "GPLv3"
    }
}

kotlin {
    compilerOptions {
        freeCompilerArgs.add("-Xcontext-parameters")
    }
}

val patchListGeneratorClasspath = configurations.create("patchListGeneratorClasspath")

dependencies {
    compileOnly(libs.gson)
    patchListGeneratorClasspath(libs.gson)
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.8.0")
}
